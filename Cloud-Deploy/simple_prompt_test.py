#!/usr/bin/env python3
"""
Simple test to check if prompts are available
"""

import asyncio
from fastmcp import Client

async def check_prompts():
    """Check what prompts are available"""
    client = Client("http://localhost:8001/mcp")

    try:
        async with client:
            print("✅ Connected to server")

            # Just list prompts
            prompts = await client.list_prompts()
            print(f"📝 Found {len(prompts)} prompts:")
            for prompt in prompts:
                print(f"  • {prompt.name}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_prompts())
