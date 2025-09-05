#!/usr/bin/env python3
"""
Debug our main server to see what's happening
"""

import asyncio
from fastmcp import Client

async def debug_server():
    client = Client("http://localhost:8001/mcp")

    try:
        async with client:
            print("✅ Connected to main server")

            # Check tools
            tools = await client.list_tools()
            print(f"🔧 Found {len(tools)} tools:")
            for tool in tools:
                print(f"  • {tool.name}")

            # Check prompts
            prompts = await client.list_prompts()
            print(f"📝 Found {len(prompts)} prompts:")
            for prompt in prompts:
                print(f"  • {prompt.name}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_server())
