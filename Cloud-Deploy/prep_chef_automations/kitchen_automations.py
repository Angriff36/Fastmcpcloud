#!/usr/bin/env python3
"""
Kitchen Automation Tools for Prep Chef
Deterministic, programmatic tools that work without AI/LLM guidance
"""

import asyncio
import json
from typing import List, Dict, Any
from fastmcp import Client

class KitchenDashboard:
    """Real-time kitchen status monitoring"""

    def __init__(self, server_url: str = "http://localhost:8001/mcp"):
        self.server_url = server_url
        self.client = Client(server_url)

    async def get_status(self) -> Dict[str, Any]:
        """Get complete kitchen status snapshot"""
        async with self.client:
            # Get all active prep lists
            prep_lists_result = await self.client.call_tool("list_prep_lists")
            prep_lists = prep_lists_result.data if hasattr(prep_lists_result, 'data') else []

            # Count active vs completed
            active_prep = len([p for p in prep_lists if isinstance(p, dict) and p.get('status') == 'active'])
            completed_prep = len([p for p in prep_lists if isinstance(p, dict) and p.get('status') == 'completed'])

            # Get inventory levels
            inventory_result = await self.client.call_tool("check_inventory")
            inventory = inventory_result.data if hasattr(inventory_result, 'data') else []

            # Count low stock items
            low_stock = len([i for i in inventory if isinstance(i, dict) and i.get('quantity', 0) < 10])

            # Get staff info
            staff_result = await self.client.call_tool("list_staff")
            staff = staff_result.data if hasattr(staff_result, 'data') else []

            # Get analytics
            stats_result = await self.client.call_tool("get_prep_stats", {"company_id": "corporate"})
            stats = stats_result.data if hasattr(stats_result, 'data') else {}

            return {
                "active_prep_lists": active_prep,
                "completed_prep_lists": completed_prep,
                "total_prep_lists": len(prep_lists),
                "low_stock_items": low_stock,
                "total_inventory_items": len(inventory),
                "staff_on_duty": len(staff),
                "completion_rate": stats.get('completed_lists', 0) / max(stats.get('total_prep_lists', 1), 1),
                "recent_activity": stats.get('recent_lists', 0),
                "timestamp": "2025-01-05T12:00:00Z"  # Would be datetime.now() in real implementation
            }

    async def get_alerts(self) -> List[str]:
        """Get urgent kitchen alerts"""
        alerts = []
        status = await self.get_status()

        if status['low_stock_items'] > 0:
            alerts.append(f"⚠️ {status['low_stock_items']} items are low in stock")

        if status['active_prep_lists'] > 10:
            alerts.append(f"🔥 High prep load: {status['active_prep_lists']} active lists")

        if status['completion_rate'] < 0.5:
            alerts.append(f"📊 Low completion rate: {status['completion_rate']:.1%}")

        return alerts


class RecipeScaler:
    """Scale recipes for different serving sizes"""

    def __init__(self, server_url: str = "http://localhost:8001/mcp"):
        self.server_url = server_url
        self.client = Client(server_url)

    def scale_ingredient_quantity(self, quantity: float, original_servings: int, new_servings: int) -> float:
        """Scale ingredient quantity proportionally"""
        return round(quantity * (new_servings / original_servings), 2)

    async def scale_recipe(self, recipe_name: str, new_servings: int) -> Dict[str, Any]:
        """Scale a recipe to new serving size"""
        async with self.client:
            # Get original recipe
            recipe_result = await self.client.call_tool("get_recipe", {"recipe_id": int(recipe_name) if recipe_name.isdigit() else 1})
            recipe = recipe_result.data if hasattr(recipe_result, 'data') else {}

            if not recipe:
                return {"error": f"Recipe '{recipe_name}' not found"}

            # Extract original servings from recipe name or assume 1
            original_servings = recipe.get('servings', 1)  # This would need to be stored in DB

            # Scale ingredients
            scaled_ingredients = []
            for ingredient in recipe.get('ingredients', []):
                if isinstance(ingredient, dict):
                    scaled_quantity = self.scale_ingredient_quantity(
                        ingredient.get('quantity', 1),
                        original_servings,
                        new_servings
                    )
                    scaled_ingredients.append({
                        **ingredient,
                        'quantity': scaled_quantity,
                        'original_quantity': ingredient.get('quantity', 1)
                    })
                else:
                    # Handle string ingredients
                    scaled_ingredients.append(ingredient)

            # Create scaled recipe name
            scaled_name = f"{recipe['name']} ({new_servings} servings)"

            # Save scaled recipe
            create_result = await self.client.call_tool("create_recipe", {
                "name": scaled_name,
                "ingredients": scaled_ingredients,
                "instructions": recipe.get('instructions', ''),
                "prep_time": recipe.get('prep_time', 0),
                "category": recipe.get('category', 'Scaled')
            })

            success = create_result.data.get('success', False) if hasattr(create_result, 'data') else False

            return {
                "original_recipe": recipe.get('name', recipe_name),
                "scaled_recipe": scaled_name,
                "original_servings": original_servings,
                "new_servings": new_servings,
                "scaling_factor": new_servings / original_servings,
                "success": success
            }


class PrepListAutomation:
    """Generate prep lists from event bookings"""

    def __init__(self, server_url: str = "http://localhost:8001/mcp"):
        self.server_url = server_url
        self.client = Client(server_url)

    async def generate_from_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate prep list from event booking data"""
        async with self.client:
            event_name = event_data.get('name', 'Unnamed Event')
            guest_count = event_data.get('guests', 50)
            event_type = event_data.get('type', 'corporate')
            menu_items = event_data.get('menu', [])

            # Calculate prep items based on guest count and menu
            prep_items = []

            # Standard per-person calculations
            for item in menu_items:
                quantity = self.calculate_quantity(item, guest_count)
                prep_item = f"{item['name']} - {item.get('prep_method', 'Prepare')} ({quantity} {item.get('unit', 'servings')}) - Event: {event_name} | Guests: {guest_count}"
                prep_items.append(prep_item)

            # Add standard event prep items (as strings)
            standard_items = self.get_standard_event_prep(guest_count, event_type)
            for item in standard_items:
                prep_item = f"{item['name']} ({item['quantity']} {item['unit']})"
                prep_items.append(prep_item)

            # Create prep list
            prep_list_result = await self.client.call_tool("create_prep_list", {
                "name": f"{event_name} - Auto Generated",
                "company_id": event_data.get('company_id', 'corporate'),
                "items": prep_items
            })

            success = prep_list_result.data.get('success', False) if hasattr(prep_list_result, 'data') else False
            prep_list_id = prep_list_result.data.get('data', {}).get('id') if hasattr(prep_list_result, 'data') else None

            return {
                "event_name": event_name,
                "guest_count": guest_count,
                "prep_list_created": success,
                "total_prep_items": len(prep_items),
                "prep_list_id": prep_list_id
            }

    def calculate_quantity(self, menu_item: Dict[str, Any], guest_count: int) -> float:
        """Calculate prep quantity based on guest count"""
        base_quantity = menu_item.get('quantity_per_person', 1)
        return round(base_quantity * guest_count, 2)

    def get_standard_event_prep(self, guest_count: int, event_type: str) -> List[Dict[str, Any]]:
        """Get standard prep items for event type"""
        standards = {
            'corporate': [
                {"name": "Coffee Service Setup", "quantity": max(guest_count // 10, 1), "unit": "urns"},
                {"name": "Water Station Setup", "quantity": max(guest_count // 20, 1), "unit": "stations"},
                {"name": "Table Settings", "quantity": guest_count, "unit": "settings"}
            ],
            'wedding': [
                {"name": "Cake Cutting Setup", "quantity": 1, "unit": "setup"},
                {"name": "Toast Setup", "quantity": max(guest_count // 50, 1), "unit": "sets"},
                {"name": "Dance Floor Prep", "quantity": 1, "unit": "area"}
            ]
        }

        return standards.get(event_type, [])


# Example usage functions
async def demo_dashboard():
    """Demonstrate kitchen dashboard"""
    print("🍳 Kitchen Dashboard Demo")
    dashboard = KitchenDashboard()

    status = await dashboard.get_status()
    alerts = await dashboard.get_alerts()

    print(f"📊 Active Prep Lists: {status['active_prep_lists']}")
    print(f"✅ Completed Lists: {status['completed_prep_lists']}")
    print(f"📦 Low Stock Items: {status['low_stock_items']}")
    print(f"👥 Staff on Duty: {status['staff_on_duty']}")
    print(f"📈 Completion Rate: {status['completion_rate']:.1%}")

    if alerts:
        print("\n🚨 Alerts:")
        for alert in alerts:
            print(f"  {alert}")
    else:
        print("\n✅ No urgent alerts")

async def demo_recipe_scaling():
    """Demonstrate recipe scaling"""
    print("\n🍽️ Recipe Scaling Demo")
    scaler = RecipeScaler()

    # Try to scale recipe ID 1 (if it exists)
    try:
        result = await scaler.scale_recipe("1", 75)
        print(f"Scaled recipe result: {result}")
    except Exception as e:
        print(f"Recipe scaling demo failed (no recipes in DB): {e}")
        print("💡 This would work with actual recipe data in your database")

async def demo_prep_automation():
    """Demonstrate prep list automation"""
    print("\n📝 Prep List Automation Demo")
    automation = PrepListAutomation()

    event_data = {
        "name": "Corporate Team Building",
        "guests": 50,
        "type": "corporate",
        "company_id": "tech_corp",
        "menu": [
            {"name": "Grilled Chicken", "quantity_per_person": 6, "unit": "oz"},
            {"name": "Quinoa Salad", "quantity_per_person": 8, "unit": "oz"}
        ]
    }

    result = await automation.generate_from_event(event_data)
    print(f"Generated prep list for: {result['event_name']}")
    print(f"Guest count: {result['guest_count']}")
    print(f"Prep items created: {result['total_prep_items']}")

async def main():
    """Run all demos"""
    await demo_dashboard()
    await demo_recipe_scaling()
    await demo_prep_automation()

if __name__ == "__main__":
    asyncio.run(main())
