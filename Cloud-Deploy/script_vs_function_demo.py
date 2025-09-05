#!/usr/bin/env python3
"""
Demonstration: Scripts vs Functions
"""

import asyncio
from prep_chef_automations import KitchenDashboard

# ========================================
# SCRIPT VERSION (Standalone)
# ========================================

def script_version():
    """This is what a script does - runs once and exits"""
    print("🏃 Script: Starting...")
    print("📊 Script: Getting kitchen status...")

    # Script logic here
    print("📊 Script: Found 3 active prep lists")
    print("⚠️ Script: 2 items low on stock")
    print("🏃 Script: Done! Exiting...")

    # Script exits here - no return value, no integration

# ========================================
# FUNCTION VERSION (Reusable)
# ========================================

async def get_kitchen_status():
    """This is what a function does - returns data for use elsewhere"""
    dashboard = KitchenDashboard("http://localhost:8001/mcp")
    status = await dashboard.get_status()
    alerts = await dashboard.get_alerts()

    return {
        "active_lists": status["active_prep_lists"],
        "low_stock": status["low_stock_items"],
        "alerts": alerts
    }

# ========================================
# INTEGRATION EXAMPLES
# ========================================

async def web_endpoint_example():
    """Function used in a web API"""
    print("🌐 Web API: Processing request...")

    # Call function instead of duplicating logic
    kitchen_data = await get_kitchen_status()

    # Use the data in API response
    response = {
        "status": "success",
        "kitchen": kitchen_data,
        "timestamp": "2025-01-05T10:00:00Z"
    }

    print(f"🌐 Web API: Returning {response}")
    return response

async def dashboard_integration_example():
    """Function used in dashboard"""
    print("📊 Dashboard: Loading data...")

    # Get kitchen data
    kitchen = await get_kitchen_status()

    # Get other dashboard data
    sales = {"today": 12500, "week": 87500}
    staff = {"on_duty": 8, "scheduled": 12}

    # Combine all data
    dashboard_data = {
        "sales": sales,
        "staff": staff,
        "kitchen": kitchen
    }

    print(f"📊 Dashboard: Combined data ready")
    return dashboard_data

async def automated_alerts_example():
    """Function used in automated system"""
    print("🤖 Automation: Checking for alerts...")

    kitchen = await get_kitchen_status()

    if kitchen["low_stock"] > 0:
        print(f"📧 Automation: Sending alert - {kitchen['low_stock']} items low")
        # send_email_alert(kitchen["alerts"])

    if kitchen["active_lists"] > 5:
        print(f"📱 Automation: Sending notification - {kitchen['active_lists']} active lists")
        # send_push_notification(f"Busy day: {kitchen['active_lists']} prep lists active")

async def main():
    print("🔄 Comparing Scripts vs Functions\n")

    # Script example
    print("📜 SCRIPT EXAMPLE:")
    script_version()
    print("❌ Script exited - data not usable by other parts of app\n")

    # Function examples
    print("🔧 FUNCTION EXAMPLES:")
    print("1. Web API Integration:")
    await web_endpoint_example()

    print("\n2. Dashboard Integration:")
    await dashboard_integration_example()

    print("\n3. Automated Alerts:")
    await automated_alerts_example()

    print("\n✅ Functions return data that can be used throughout your app!")
    print("✅ Functions can be called from web endpoints, scheduled jobs, other functions")
    print("✅ Functions enable integration - scripts are standalone")

if __name__ == "__main__":
    asyncio.run(main())
