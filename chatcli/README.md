# ChatCLI

An interactive CLI chat application that uses OpenAI models to provide intelligent responses

## Installation

```bash
pip install chatcli
```

Or for development:

```bash
git clone https://github.com/doover17/ChatCLI.git.git
cd chatcli
pip install -e .
```

## Environment Setup

Create a `.env` file in the root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

```bash
chatcli --help
```

### Commands

#### hello

```bash
chatcli hello --name YourName
chatcli hello --name YourName --ai
```

## Development

### Running Tests

```bash
pytest
```

## License

MIT
