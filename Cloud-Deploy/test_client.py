#!/usr/bin/env python3
"""
Test FastMCP Client with our Prep Chef Database Server
Demonstrates programmatic access to kitchen management tools
"""

import asyncio
from fastmcp import Client

async def test_prep_chef_client():
    """Test our Prep Chef server using the FastMCP Client"""

    print("🍳 Testing FastMCP Client with Prep Chef Database Server")
    print("=" * 60)

    # Connect to our local server
    client = Client("http://localhost:8001/mcp")

    try:
        async with client:
            print("✅ Connected to Prep Chef server")

            # Test basic connectivity
            await client.ping()
            print("✅ Server ping successful")

            # List available tools
            print("\n📋 Available Kitchen Management Tools:")
            tools = await client.list_tools()
            for tool in tools:
                print(f"  • {tool.name}: {tool.description}")

            # Test listing prep lists
            print("\n📝 Testing prep list operations...")

            # First, let's see if we can call the tools (they may fail without proper DB setup)
            try:
                result = await client.call_tool("list_prep_lists")
                print(f"✅ Successfully called list_prep_lists")
                print(f"   Result: {result}")
            except Exception as e:
                print(f"⚠️  list_prep_lists failed (expected without DB): {e}")

            # Test database connection tool
            try:
                result = await client.call_tool("test_database_connection")
                print(f"✅ Database connection test result: {result}")
            except Exception as e:
                print(f"⚠️  Database connection test failed: {e}")

            # Test getting database schema
            try:
                result = await client.call_tool("get_database_schema")
                print(f"✅ Database schema info: {result}")
            except Exception as e:
                print(f"⚠️  Schema retrieval failed: {e}")

    except Exception as e:
        print(f"❌ Client error: {e}")
        print("💡 Make sure the server is running on http://localhost:8001/mcp")

    print("\n🎉 Client test completed!")

if __name__ == "__main__":
    asyncio.run(test_prep_chef_client())
