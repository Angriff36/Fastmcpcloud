#!/usr/bin/env python3
"""
Integration Guide: Connecting Your App to FastMCP Automations
Multiple integration patterns for different app architectures
"""

# ========================================
# Pattern 1: Direct Import (Simplest)
# ========================================

def direct_import_integration():
    """
    If you have a Python app, import and use directly
    """
    from kitchen_automations import KitchenDashboard, PrepListAutomation

    async def handle_event_booking(event_data):
        # Your existing booking logic
        # ...

        # Add automation
        automation = PrepListAutomation("http://localhost:8001/mcp")
        result = await automation.generate_from_event(event_data)

        return {"booking": "created", "prep_list": result}

# ========================================
# Pattern 2: HTTP API Integration
# ========================================

def http_api_integration():
    """
    If your app is in a different language (Node.js, Java, etc.)
    Make HTTP calls to the automation API
    """
    import requests
    import json

    def book_event_with_prep(event_data):
        # Your existing booking logic
        # ...

        # Call automation API
        response = requests.post(
            "http://localhost:8000/api/events/book",
            json=event_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Prep list generated: {result['prep_list_generation']}")

        return booking_result

# ========================================
# Pattern 3: Webhook Integration
# ========================================

def webhook_integration():
    """
    Have external systems call your automation via webhooks
    """
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route('/webhook/booking-system', methods=['POST'])
    def handle_booking_webhook():
        event_data = request.json

        # Trigger automation asynchronously
        # (In production, use Celery, RQ, or similar)

        from kitchen_automations import PrepListAutomation
        import asyncio

        async def generate_prep():
            automation = PrepListAutomation("http://localhost:8001/mcp")
            result = await automation.generate_from_event(event_data)
            print(f"Generated prep list for {result['event_name']}")

        # Run in background (simplified - use proper task queue in production)
        asyncio.run(generate_prep())

        return jsonify({"status": "prep_list_generation_started"})

# ========================================
# Pattern 4: Database Trigger Integration
# ========================================

def database_trigger_integration():
    """
    If your app uses PostgreSQL, set up database triggers
    """
    sql_trigger = """
    CREATE OR REPLACE FUNCTION generate_prep_list()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Call your automation API when new event is inserted
        PERFORM pg_notify('new_event', row_to_json(NEW)::text);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER event_prep_trigger
        AFTER INSERT ON events
        FOR EACH ROW
        EXECUTE FUNCTION generate_prep_list();
    """

    # Then listen for notifications in your app
    def listen_for_events():
        import psycopg2
        import select

        conn = psycopg2.connect("your_database_url")
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        curs = conn.cursor()
        curs.execute("LISTEN new_event;")

        while True:
            select.select([conn], [], [])
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                event_data = json.loads(notify.payload)

                # Generate prep list
                automation = PrepListAutomation("http://localhost:8001/mcp")
                asyncio.run(automation.generate_from_event(event_data))

# ========================================
# Pattern 5: Cron Job Integration
# ========================================

def cron_job_integration():
    """
    Set up scheduled tasks for regular kitchen operations
    """
    cron_jobs = """
    # Daily kitchen status report at 6 AM
    0 6 * * * python -c "from integration_guide import daily_report; daily_report()"

    # Check inventory every 2 hours
    0 */2 * * * python -c "from integration_guide import check_inventory; check_inventory()"

    # Generate weekly analytics on Monday at 9 AM
    0 9 * * 1 python -c "from integration_guide import weekly_analytics; weekly_analytics()"
    """

    async def daily_report():
        from kitchen_automations import KitchenDashboard
        dashboard = KitchenDashboard("http://localhost:8001/mcp")
        status = await dashboard.get_status()
        alerts = await dashboard.get_alerts()

        # Send email/Slack notification
        send_notification(f"Daily Report: {status['active_prep_lists']} active lists")

    async def check_inventory():
        from kitchen_automations import KitchenDashboard
        dashboard = KitchenDashboard("http://localhost:8001/mcp")
        status = await dashboard.get_status()

        if status['low_stock_items'] > 0:
            send_alert(f"{status['low_stock_items']} items low in stock")

# ========================================
# Pattern 6: Message Queue Integration
# ========================================

def message_queue_integration():
    """
    Use Redis, RabbitMQ, or similar for async processing
    """
    import redis
    import json

    def queue_prep_generation(event_data):
        # Add to Redis queue
        r = redis.Redis()
        r.lpush('prep_generation_queue', json.dumps(event_data))

    def process_prep_queue():
        from kitchen_automations import PrepListAutomation

        r = redis.Redis()
        automation = PrepListAutomation("http://localhost:8001/mcp")

        while True:
            # Get next job from queue
            _, job_data = r.brpop('prep_generation_queue')
            event_data = json.loads(job_data)

            # Process job
            asyncio.run(automation.generate_from_event(event_data))

# ========================================
# Quick Start Integration Examples
# ========================================

async def quick_start_examples():
    """
    Copy-paste examples for immediate integration
    """
    from kitchen_automations import KitchenDashboard, PrepListAutomation, RecipeScaler

    # Example 1: Add to existing booking function
    async def book_event_with_prep(event_data):
        # Your existing booking code here
        # booking = await create_booking(event_data)

        # Add automation
        automation = PrepListAutomation("http://localhost:8001/mcp")
        prep_result = await automation.generate_from_event(event_data)

        return {
            "booking": "success",
            "prep_list_items": prep_result["total_prep_items"]
        }

    # Example 2: Add to existing dashboard
    async def enhanced_dashboard():
        # Your existing dashboard data
        # data = await get_dashboard_data()

        # Add kitchen status
        dashboard = KitchenDashboard("http://localhost:8001/mcp")
        kitchen_status = await dashboard.get_status()
        kitchen_alerts = await dashboard.get_alerts()

        return {
            "your_existing_data": "...",
            "kitchen": {
                "active_lists": kitchen_status["active_prep_lists"],
                "alerts": kitchen_alerts
            }
        }

    # Example 3: Recipe scaling in order management
    async def handle_large_order(order_data):
        servings_needed = order_data["guest_count"]

        scaler = RecipeScaler("http://localhost:8001/mcp")
        scaled_recipe = await scaler.scale_recipe(
            str(order_data["recipe_id"]),
            servings_needed
        )

        return scaled_recipe

if __name__ == "__main__":
    print("🚀 FastMCP Integration Guide")
    print("Choose the integration pattern that fits your app architecture:")
    print("1. Direct Import - For Python apps")
    print("2. HTTP API - For any language")
    print("3. Webhooks - For external integrations")
    print("4. Database Triggers - For PostgreSQL apps")
    print("5. Cron Jobs - For scheduled tasks")
    print("6. Message Queues - For async processing")
    print("\n📚 See app_integration.py for a complete FastAPI example")
