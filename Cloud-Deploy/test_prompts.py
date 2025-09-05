#!/usr/bin/env python3
"""
Test FastMCP Prompts with our Prep Chef Server
Demonstrates reusable prompt templates for kitchen guidance
"""

import asyncio
from fastmcp import Client

async def test_prompts():
    """Test our kitchen prompts"""

    print("🍳 Testing FastMCP Prompts - Prep Chef Kitchen Guidance")
    print("=" * 60)

    client = Client("http://localhost:8001/mcp")

    try:
        async with client:
            print("✅ Connected to Prep Chef server")

            # List available prompts
            print("\n📝 Available Kitchen Guidance Prompts:")
            prompts = await client.list_prompts()
            for prompt in prompts:
                print(f"  • {prompt.name}: {prompt.description}")

            # Test recipe analysis prompt
            print("\n🍽️ Testing Recipe Analysis Prompt:")
            recipe_result = await client.get_prompt("recipe_analysis", {
                "recipe_name": "Grilled Salmon with Herb Butter",
                "analysis_type": "nutritional value"
            })
            print("Generated prompt:")
            for message in recipe_result.messages:
                print(f"  {message.content.text}")

            # Test prep guidance prompt
            print("\n📋 Testing Prep Guidance Prompt:")
            prep_result = await client.get_prompt("prep_guidance", {
                "event_type": "wedding reception",
                "guest_count": 150,
                "dietary_requirements": "vegetarian options, gluten-free"
            })
            print("Generated prompt:")
            for message in prep_result.messages:
                print(f"  {message.content.text}")

            # Test menu planning prompt
            print("\n📋 Testing Menu Planning Prompt:")
            menu_result = await client.get_prompt("menu_planning", {
                "occasion": "corporate team building",
                "guest_count": 50,
                "budget": "moderate",
                "cuisine_type": "American"
            })
            print("Generated prompt:")
            for message in menu_result.messages:
                print(f"  {message.content.text}")

            # Test quality control prompt
            print("\n🔍 Testing Quality Control Prompt:")
            qc_result = await client.get_prompt("quality_control_check", {
                "station": "grill",
                "checklist_type": "pre-service"
            })
            print("Generated prompt:")
            for message in qc_result.messages:
                print(f"  {message.content.text}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure the server is running on http://localhost:8001/mcp")

    print("\n🎉 Prompts testing completed!")

if __name__ == "__main__":
    asyncio.run(test_prompts())
