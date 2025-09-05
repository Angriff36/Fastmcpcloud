#!/usr/bin/env python3
"""
How to use the packaged Prep Chef Automations in your app
"""

import asyncio
from prep_chef_automations import KitchenDashboard, PrepListAutomation, RecipeScaler

async def example_usage():
    """Example of how to use the packaged automations"""

    # Initialize tools (use your server URL)
    dashboard = KitchenDashboard("http://localhost:8001/mcp")
    prep_automation = PrepListAutomation("http://localhost:8001/mcp")
    recipe_scaler = RecipeScaler("http://localhost:8001/mcp")

    # Get kitchen status
    status = await dashboard.get_status()
    alerts = await dashboard.get_alerts()

    print(f"Active prep lists: {status['active_prep_lists']}")
    print(f"Low stock items: {status['low_stock_items']}")
    print(f"Alerts: {alerts}")

    # Generate prep list for an event
    event_data = {
        "name": "Corporate Lunch",
        "guests": 25,
        "type": "corporate",
        "menu": [
            {"name": "Grilled Chicken", "quantity_per_person": 6, "unit": "oz"},
            {"name": "Caesar Salad", "quantity_per_person": 8, "unit": "oz"}
        ]
    }

    prep_result = await prep_automation.generate_from_event(event_data)
    print(f"Generated prep list with {prep_result['total_prep_items']} items")

    # Scale a recipe
    try:
        scaled = await recipe_scaler.scale_recipe("1", 50)
        print(f"Scaled recipe: {scaled.get('scaled_recipe', 'N/A')}")
    except Exception as e:
        print(f"Recipe scaling: {e}")

if __name__ == "__main__":
    asyncio.run(example_usage())
