# Prep Chef Automations Package

Kitchen automation tools that work **without AI/LLM guidance**. Pure business logic for restaurant operations.

## 🚀 **Installation**

### Option 1: Install from source
```bash
# Clone/download the package
cd /path/to/prep-chef-automations

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Option 2: Copy to your project
```bash
# Copy the prep_chef_automations folder to your project
cp -r prep_chef_automations /path/to/your/app/

# Install dependencies
pip install fastmcp pydantic httpx
```

## 📦 **Usage**

### Basic Import
```python
from prep_chef_automations import KitchenDashboard, PrepListAutomation, RecipeScaler
```

### Initialize Tools
```python
# Connect to your MCP server
dashboard = KitchenDashboard("http://localhost:8001/mcp")
prep_automation = PrepListAutomation("http://localhost:8001/mcp")
recipe_scaler = RecipeScaler("http://localhost:8001/mcp")
```

### Kitchen Dashboard
```python
# Get real-time status
status = await dashboard.get_status()
alerts = await dashboard.get_alerts()

print(f"Active lists: {status['active_prep_lists']}")
print(f"Low stock: {status['low_stock_items']}")
print(f"Alerts: {alerts}")
```

### Prep List Automation
```python
# Generate prep list from event booking
event_data = {
    "name": "Corporate Event",
    "guests": 50,
    "type": "corporate",
    "menu": [
        {"name": "Grilled Chicken", "quantity_per_person": 6, "unit": "oz"},
        {"name": "Caesar Salad", "quantity_per_person": 8, "unit": "oz"}
    ]
}

result = await prep_automation.generate_from_event(event_data)
print(f"Created {result['total_prep_items']} prep items")
```

### Recipe Scaling
```python
# Scale recipe for different serving sizes
scaled = await recipe_scaler.scale_recipe("1", 75)
print(f"Scaled to: {scaled['scaled_recipe']}")
```

## 🔧 **Integration Examples**

### Add to Existing Booking Flow
```python
async def create_booking(booking_data):
    # Your existing booking logic
    booking = await save_to_database(booking_data)

    # Add automation
    automation = PrepListAutomation("http://localhost:8001/mcp")
    await automation.generate_from_event(booking_data)

    return booking
```

### Add to Dashboard
```python
async def get_dashboard_data():
    # Your existing data
    data = await get_existing_dashboard()

    # Add kitchen status
    dashboard = KitchenDashboard("http://localhost:8001/mcp")
    kitchen_status = await dashboard.get_status()

    data['kitchen'] = kitchen_status
    return data
```

### Cron Job for Daily Reports
```bash
# Add to crontab
0 6 * * * python -c "from prep_chef_automations import KitchenDashboard; import asyncio; asyncio.run(daily_report())"
```

## 🎯 **What You Get**

- ✅ **No AI/LLM required** - Pure business logic
- ✅ **Deterministic operations** - Predictable results
- ✅ **Easy integration** - Simple import and use
- ✅ **Type safety** - Full type hints and validation
- ✅ **Async support** - Modern Python async/await
- ✅ **Error handling** - Graceful failure handling
- ✅ **Extensible** - Easy to add new automations

## 📋 **Requirements**

- Python 3.8+
- FastMCP server running
- Dependencies: `fastmcp`, `pydantic`, `httpx`

## 🏃 **Quick Test**

```bash
# Run the usage example
python usage_example.py
```

## 📚 **API Reference**

### KitchenDashboard
- `get_status()` - Get complete kitchen status
- `get_alerts()` - Get urgent alerts

### PrepListAutomation
- `generate_from_event(event_data)` - Create prep list from event

### RecipeScaler
- `scale_recipe(recipe_id, new_servings)` - Scale recipe to new size

## 🔒 **Security**

- No sensitive data stored in package
- All operations go through your MCP server
- Environment variables for configuration
- No external API calls (except to your MCP server)

## 📞 **Support**

Package contains pure business logic - no AI/LLM dependencies.
All operations are deterministic and testable.
