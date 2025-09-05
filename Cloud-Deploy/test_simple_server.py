#!/usr/bin/env python3
"""
Test the simple server with tool and prompt
"""

import asyncio
from fastmcp import Client

async def test_simple():
    client = Client("http://localhost:8003/mcp")

    try:
        async with client:
            print("✅ Connected to simple server")

            # Check tools
            tools = await client.list_tools()
            print(f"🔧 Found {len(tools)} tools:")
            for tool in tools:
                print(f"  • {tool.name}: {tool.description}")

            # Check prompts
            prompts = await client.list_prompts()
            print(f"📝 Found {len(prompts)} prompts:")
            for prompt in prompts:
                print(f"  • {prompt.name}: {prompt.description}")

            # Test tool
            if tools:
                result = await client.call_tool("test_tool")
                print(f"Tool result: {result}")

            # Test prompt
            if prompts:
                result = await client.get_prompt("test_prompt", {"message": "Hello from test!"})
                print("Prompt result:")
                for message in result.messages:
                    print(f"  {message.content.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_simple())
