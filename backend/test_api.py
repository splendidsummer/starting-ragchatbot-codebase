#!/usr/bin/env python3
"""Quick test script to check API compatibility"""

import os
from dotenv import load_dotenv
import anthropic

# Load environment variables (override system vars)
load_dotenv("../.env", override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")
base_url = os.getenv("ANTHROPIC_BASE_URL")
model = os.getenv("ANTHROPIC_MODEL")

print(f"Testing API with:")
print(f"  Base URL: {base_url}")
print(f"  Model: {model}")
print()

# Create client
client = anthropic.Anthropic(api_key=api_key, base_url=base_url)

# Test 1: Simple message without tools
print("Test 1: Simple message (no tools)")
try:
    response = client.messages.create(
        model=model,
        max_tokens=100,
        messages=[{"role": "user", "content": "Say hello"}]
    )
    print(f"✓ Success: {response.content[0].text}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 2: Message with tools
print("Test 2: Message with tool calling")
try:
    tools = [{
        "name": "test_tool",
        "description": "A test tool",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Test query"}
            },
            "required": ["query"]
        }
    }]

    response = client.messages.create(
        model=model,
        max_tokens=100,
        messages=[{"role": "user", "content": "Use the test tool with query 'hello'"}],
        tools=tools,
        tool_choice={"type": "auto"}
    )
    print(f"✓ Success: stop_reason={response.stop_reason}")
    print(f"  Content: {response.content}")
except Exception as e:
    print(f"✗ Error: {e}")