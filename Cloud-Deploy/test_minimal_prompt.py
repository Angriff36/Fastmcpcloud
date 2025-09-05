#!/usr/bin/env python3
"""
Test the minimal prompt server
"""

import asyncio
from fastmcp import Client

async def test_minimal():
    client = Client("http://localhost:8002/mcp")

    try:
        async with client:
            print("✅ Connected to minimal server")

            prompts = await client.list_prompts()
            print(f"📝 Found {len(prompts)} prompts:")
            for prompt in prompts:
                print(f"  • {prompt.name}: {prompt.description}")

            if prompts:
                # Test getting the prompt
                result = await client.get_prompt("test_prompt", {"message": "Hello World"})
                print("Generated prompt:")
                for message in result.messages:
                    print(f"  {message.content.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_minimal())
