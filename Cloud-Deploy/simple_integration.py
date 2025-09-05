#!/usr/bin/env python3
"""
Simple integration example for your app
"""

import asyncio
from prep_chef_automations import KitchenDashboard, PrepListAutomation

async def integrate_into_your_app():
    """Example of how to integrate into your existing app"""

    # Initialize (use your server URL)
    dashboard = KitchenDashboard("http://localhost:8001/mcp")
    prep_automation = PrepListAutomation("http://localhost:8001/mcp")

    # Example: Add to your booking flow
    async def book_event(event_data):
        # Your existing booking logic here
        print(f"Booking event: {event_data['name']}")

        # Add automation
        result = await prep_automation.generate_from_event(event_data)
        print(f"✅ Generated prep list with {result['total_prep_items']} items")

        return {"booking": "success", "prep_list": result}

    # Example: Add to your dashboard
    async def get_enhanced_dashboard():
        # Your existing dashboard data
        dashboard_data = {"existing": "data"}

        # Add kitchen status
        status = await dashboard.get_status()
        alerts = await dashboard.get_alerts()

        dashboard_data["kitchen"] = {
            "active_lists": status["active_prep_lists"],
            "alerts": alerts
        }

        return dashboard_data

    # Test the integration
    print("🧪 Testing integration...")

    # Test dashboard
    status = await dashboard.get_status()
    print(f"📊 Kitchen status: {status['active_prep_lists']} active lists")

    # Test prep automation
    test_event = {
        "name": "Test Event",
        "guests": 10,
        "type": "corporate",
        "menu": [{"name": "Test Item", "quantity_per_person": 1, "unit": "each"}]
    }

    result = await prep_automation.generate_from_event(test_event)
    print(f"📝 Generated {result['total_prep_items']} prep items")

if __name__ == "__main__":
    asyncio.run(integrate_into_your_app())
