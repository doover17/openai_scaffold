from textual.app import App, ComposeResult
from textual.containers import Container, ScrollableContainer
from textual.widgets import Header, Footer, Input, Static, Button
from textual.binding import Binding
from openai import OpenAI
import os
import json
from datetime import datetime
from pathlib import Path

class Message(Static):
    """A chat message."""

    def __init__(self, sender: str, content: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sender = sender
        self.content = content

    def compose(self) -> ComposeResult:
        if self.sender == "user":
            yield Static(f"You: {self.content}", classes="user-message")
        elif self.sender == "assistant":
            yield Static(f"Assistant: {self.content}", classes="assistant-message")
        else:
            yield Static(f"System: {self.content}", classes="system-message")


class ChatCLIApp(App):
    """Textual TUI app for ChatCLI."""

    CSS = """
    Screen {
        background: #0f0f0f;
    }

    Header {
        dock: top;
        height: 1;
        background: #3c3c3c;
        color: white;
    }

    Footer {
        dock: bottom;
        height: 1;
        background: #3c3c3c;
        color: white;
    }

    #chat-container {
        width: 100%;
        height: 100%;
    }

    #message-container {
        width: 100%;
        height: 1fr;
        border: solid #3c3c3c;
        background: #1e1e1e;
        overflow-y: scroll;
    }

    #input-container {
        width: 100%;
        height: 3;
        layout: horizontal;
    }

    Input {
        width: 1fr;
        height: 3;
    }

    Button {
        width: 10;
        height: 3;
    }

    .user-message {
        background: #2a4d6e;
        color: white;
        padding: 1;
        margin: 1 0;
        border: solid #3c3c3c;
    }

    .assistant-message {
        background: #2e4f3a;
        color: white;
        padding: 1;
        margin: 1 0;
        border: solid #3c3c3c;
    }

    .system-message {
        color: #999999;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+s", "save_history", "Save History"),
        Binding("ctrl+c", "copy_last", "Copy Last Message"),
        Binding("f1", "help", "Help"),
        Binding("ctrl+n", "new_chat", "New Chat"),
        Binding("ctrl+l", "clear", "Clear Screen"),
        Binding("ctrl+up", "previous_chat", "Previous Chat"),
        Binding("ctrl+down", "next_chat", "Next Chat"),
    ]

    def __init__(self, history_file="~/.chatcli_history.json", model="gpt-4o-mini"):
        super().__init__()
        self.history_file = Path(os.path.expanduser(history_file))
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.conversation = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "created_at": datetime.now().isoformat(),
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful assistant responding to queries from the command line."
                }
            ]
        }
        self.load_history()

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header(show_clock=True)
        with Container(id="chat-container"):
            with ScrollableContainer(id="message-container"):
                # Messages will be added here
                pass
            with Container(id="input-container"):
                yield Input(placeholder="Type your message here...", id="user-input")
                yield Button("Send", id="send-button", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        """Event handler called when app is mounted."""
        self.query_one("#user-input").focus()
        # Add welcome message
        self.add_message("system", "Welcome to ChatCLI! Type your message and press Enter.")

    def add_message(self, sender, content):
        """Add a message to the chat."""
        message = Message(sender, content)
        self.query_one("#message-container").mount(message)
        self.query_one("#message-container").scroll_end()
        
        # Add to conversation history if it's a user or assistant message
        if sender in ["user", "assistant"]:
            self.conversation["messages"].append({
                "role": sender,
                "content": content
            })

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler for button press."""
        if event.button.id == "send-button":
            await self.send_message()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Event handler for input submission."""
        await self.send_message()

    async def send_message(self) -> None:
        """Send user message and get AI response."""
        user_input = self.query_one("#user-input").value
        if not user_input:
            return
        
        # Clear input
        self.query_one("#user-input").value = ""
        
        # Add user message
        self.add_message("user", user_input)
        
        try:
            # Show "thinking" message
            self.add_message("system", "Thinking...")
            
            # Prepare the API parameters
            api_params = {
                "model": self.model,
                "messages": [
                    {"role": m["role"], "content": m["content"]} 
                    for m in self.conversation["messages"]
                ]
            }
            
            # Create a worker that runs in a thread
            def make_api_call():
                return self.client.chat.completions.create(**api_params)
            
            # This is the key fix - use thread=True to run in a separate thread
            worker = self.run_worker(make_api_call, thread=True)
            
            # Wait for the worker to complete
            response = await worker.wait()
            
            
            # Add assistant message
            assistant_message = response.choices[0].message.content
            self.add_message("assistant", assistant_message)
            
            # Save history
            self.save_history()
            
        except Exception as e:
            self.add_message("system", f"Error: {str(e)}")

    def action_save_history(self) -> None:
        """Save chat history."""
        self.save_history()
        self.add_message("system", "Chat history saved.")

    def action_copy_last(self) -> None:
        """Copy the last message to clipboard."""
        if len(self.conversation["messages"]) > 1:
            last_message = self.conversation["messages"][-1]["content"]
            self.app.clipboard = last_message
            self.add_message("system", "Last message copied to clipboard.")

    def action_help(self) -> None:
        """Show help information."""
        help_text = """
        ChatCLI Keyboard Shortcuts:
        - Ctrl+Q: Quit the application
        - Ctrl+S: Save conversation history
        - Ctrl+C: Copy last message to clipboard
        - F1: Show this help message
        - Ctrl+N: New chat
        - Ctrl+L: Clear screen
        - Ctrl+Up: Previous chat
        - Ctrl+Down: Next chat
        """
        self.add_message("system", help_text)
        
    def action_clear(self) -> None:
        """Clear the chat screen."""
        message_container = self.query_one("#message-container")
        message_container.remove_children()
        self.add_message("system", "Chat cleared.")

    def action_new_chat(self) -> None:
        """Start a new chat."""
        self.conversation = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "created_at": datetime.now().isoformat(),
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful assistant responding to queries from the command line."
                }
            ]
        }
        self.action_clear()
        self.add_message("system", "New chat started.")
        
    def action_previous_chat(self) -> None:
        """Navigate to previous chat in history."""
        # Implement this functionality
        self.add_message("system", "Previous chat navigation not implemented yet.")
        
    def action_next_chat(self) -> None:
        """Navigate to next chat in history."""
        # Implement this functionality
        self.add_message("system", "Next chat navigation not implemented yet.")

    def load_history(self) -> None:
        """Load chat history if exists."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
                    if history:
                        # Take the latest conversation
                        self.conversation = history[-1]
            except json.JSONDecodeError:
                pass  # Use the default initialized conversation

    def save_history(self) -> None:
        """Save chat history to file."""
        history = []
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                pass
        
        # Find existing conversation or add new one
        found = False
        for i, conv in enumerate(history):
            if conv["id"] == self.conversation["id"]:
                history[i] = self.conversation
                found = True
                break
        
        if not found:
            history.append(self.conversation)
        
        # Save to file
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)


def run_tui(history_file="~/.chatcli_history.json", model="gpt-4o-mini"):
    """Run the Textual TUI app."""
    app = ChatCLIApp(history_file=history_file, model=model)
    app.run()


if __name__ == "__main__":
    run_tui()