from openai import OpenAI
import os

client = OpenAI()
models = client.models.list()

print("Available models:")
for model in models:
    print(model.id)