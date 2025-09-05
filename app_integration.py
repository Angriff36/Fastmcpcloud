#!/usr/bin/env python3
"""
App Integration Examples for Prep Chef FastMCP Server
Shows how to connect your existing app to the automation tools
"""

import asyncio
import json
from typing import Dict, Any, List
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from kitchen_automations import KitchenDashboard, RecipeScaler, PrepListAutomation

# Example FastAPI app integration
app = FastAPI(title="Prep Chef App Integration")

# Initialize automation tools
dashboard = KitchenDashboard("http://localhost:8001/mcp")
recipe_scaler = RecipeScaler("http://localhost:8001/mcp")
prep_automation = PrepListAutomation("http://localhost:8001/mcp")

# Pydantic models for API
class EventBooking(BaseModel):
    name: str
    guests: int
    type: str = "corporate"
    company_id: str = "corporate"
    menu: List[Dict[str, Any]] = []

class RecipeScaleRequest(BaseModel):
    recipe_id: int
    new_servings: int

class DashboardResponse(BaseModel):
    active_prep_lists: int
    completed_prep_lists: int
    total_prep_lists: int
    low_stock_items: int
    total_inventory_items: int
    staff_on_duty: int
    completion_rate: float
    alerts: List[str]

# API Endpoints for your app
@app.get("/api/kitchen/status", response_model=DashboardResponse)
async def get_kitchen_status():
    """Get real-time kitchen status for your app dashboard"""
    try:
        status = await dashboard.get_status()
        alerts = await dashboard.get_alerts()

        return DashboardResponse(
            active_prep_lists=status["active_prep_lists"],
            completed_prep_lists=status["completed_prep_lists"],
            total_prep_lists=status["total_prep_lists"],
            low_stock_items=status["low_stock_items"],
            total_inventory_items=status["total_inventory_items"],
            staff_on_duty=status["staff_on_duty"],
            completion_rate=status["completion_rate"],
            alerts=alerts
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kitchen status error: {str(e)}")

@app.post("/api/events/book")
async def book_event(event: EventBooking, background_tasks: BackgroundTasks):
    """Book an event and automatically generate prep list"""
    try:
        # Convert Pydantic model to dict for automation
        event_data = event.dict()

        # Run prep list generation in background
        background_tasks.add_task(generate_prep_list_background, event_data)

        return {
            "message": "Event booked successfully",
            "prep_list_generation": "started",
            "event_name": event.name,
            "guests": event.guests
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event booking error: {str(e)}")

@app.post("/api/recipes/scale")
async def scale_recipe(request: RecipeScaleRequest):
    """Scale a recipe for different serving sizes"""
    try:
        result = await recipe_scaler.scale_recipe(str(request.recipe_id), request.new_servings)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return {
            "message": "Recipe scaled successfully",
            "original_recipe": result["original_recipe"],
            "scaled_recipe": result["scaled_recipe"],
            "new_servings": request.new_servings,
            "scaling_factor": result["scaling_factor"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recipe scaling error: {str(e)}")

@app.post("/api/webhook/event-booked")
async def event_booked_webhook(event_data: Dict[str, Any]):
    """Webhook endpoint for external booking systems"""
    try:
        result = await prep_automation.generate_from_event(event_data)

        return {
            "message": "Prep list generated from webhook",
            "event_name": result["event_name"],
            "guest_count": result["guest_count"],
            "prep_list_created": result["prep_list_created"],
            "total_prep_items": result["total_prep_items"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing error: {str(e)}")

# Background task function
async def generate_prep_list_background(event_data: Dict[str, Any]):
    """Background task to generate prep list without blocking API response"""
    try:
        result = await prep_automation.generate_from_event(event_data)
        print(f"✅ Prep list generated for {result['event_name']}: {result['total_prep_items']} items")
    except Exception as e:
        print(f"❌ Failed to generate prep list: {str(e)}")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check for your app"""
    try:
        # Test connection to MCP server
        await dashboard.get_status()
        return {"status": "healthy", "mcp_server": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "mcp_server": f"error: {str(e)}"}

# Example usage in your existing app
def integrate_with_existing_app():
    """
    How to integrate these tools into your existing application
    """

    # Example 1: Add to existing booking flow
    """
    # In your existing booking controller
    async def create_booking(booking_data):
        # Your existing booking logic
        booking = await create_booking_in_db(booking_data)

        # Add automation
        if booking_data.get('auto_generate_prep', True):
            automation = PrepListAutomation("http://localhost:8001/mcp")
            await automation.generate_from_event({
                'name': booking.event_name,
                'guests': booking.guest_count,
                'type': booking.event_type,
                'menu': booking.menu_items
            })

        return booking
    """

    # Example 2: Add to existing dashboard
    """
    # In your existing dashboard controller
    async def get_dashboard_data():
        # Your existing dashboard data
        data = await get_existing_dashboard_data()

        # Add kitchen automation data
        try:
            dashboard = KitchenDashboard("http://localhost:8001/mcp")
            kitchen_status = await dashboard.get_status()
            kitchen_alerts = await dashboard.get_alerts()

            data['kitchen'] = {
                'status': kitchen_status,
                'alerts': kitchen_alerts
            }
        except Exception as e:
            data['kitchen'] = {'error': str(e)}

        return data
    """

    # Example 3: Cron job for daily tasks
    """
    # Add to your crontab (runs daily at 6 AM)
    # 0 6 * * * python -c "from app_integration import daily_kitchen_report; asyncio.run(daily_kitchen_report())"
    """

async def daily_kitchen_report():
    """Daily kitchen report function for cron jobs"""
    try:
        status = await dashboard.get_status()
        alerts = await dashboard.get_alerts()

        report = f"""
        📊 Daily Kitchen Report
        Active Prep Lists: {status['active_prep_lists']}
        Low Stock Items: {status['low_stock_items']}
        Completion Rate: {status['completion_rate']:.1%}
        Alerts: {len(alerts)}
        """

        # Send email or Slack notification
        print(report)

    except Exception as e:
        print(f"Daily report failed: {str(e)}")

if __name__ == "__main__":
    # Run the FastAPI server
    import uvicorn
    print("🚀 Starting Prep Chef App Integration Server")
    print("📡 API available at: http://localhost:8000")
    print("📊 Kitchen Dashboard: http://localhost:8000/api/kitchen/status")
    print("🎫 Event Booking: POST to http://localhost:8000/api/events/book")
    print("🍽️ Recipe Scaling: POST to http://localhost:8000/api/recipes/scale")
    uvicorn.run(app, host="0.0.0.0", port=8000)

