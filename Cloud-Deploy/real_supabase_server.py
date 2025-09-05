#!/usr/bin/env python3
"""
Real FastMCP server that connects to your Supabase database.
Replace the table names and operations with your actual Supabase setup.
"""

import os
from fastmcp import FastMCP
from supabase import create_client
from typing import List, Dict, Any, Optional
import json

# Initialize FastMCP server
mcp = FastMCP("Prep Chef Database Server")
print("🚀 FastMCP server initialized")  # Debug print

# Add prompt immediately after initialization
@mcp.prompt
def kitchen_guidance(task: str = "general prep") -> str:
    """Generate kitchen guidance prompts."""
    print(f"🎯 Prompt called with task: {task}")  # Debug print
    return f"Please provide guidance for kitchen task: {task}"

print("📝 Prompt registered")  # Debug print

# Get Supabase credentials from environment variables with CORRECT fallbacks
SUPABASE_URL = os.getenv("SUPABASE_URL") or "https://zdqkhjwxzkpjokcidera.supabase.co"
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpkcWtoand4emtwam9rY2lkZXJhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1MjQ4NzMsImV4cCI6MjA3MTEwMDg3M30.owzBF395ohMPs9PP72GF7VUc9Pb9V9Lml_jRSG8oMhY"

def get_supabase_client():
    """Create and return Supabase client"""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_ANON_KEY environment variables")

    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ============================================================================
# SUPABASE DATABASE TOOLS - Customize these for your tables!
# ============================================================================

@mcp.tool
def list_prep_lists(company_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all prep lists, optionally filtered by company"""
    try:
        supabase = get_supabase_client()
        query = supabase.table('prep_lists').select('*')

        if company_id:
            query = query.eq('company_id', company_id)

        result = query.execute()
        return result.data
    except Exception as e:
        return [{"error": f"Failed to fetch prep lists: {str(e)}"}]

@mcp.tool
def get_prep_list(list_id: int) -> Dict[str, Any]:
    """Get a specific prep list by ID"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('prep_lists').select('*').eq('id', list_id).execute()

        if result.data:
            return result.data[0]
        else:
            return {"error": f"Prep list {list_id} not found"}
    except Exception as e:
        return {"error": f"Failed to fetch prep list: {str(e)}"}

@mcp.tool
def create_prep_list(name: str, company_id: str, items: List[str] = None) -> Dict[str, Any]:
    """Create a new prep list"""
    try:
        supabase = get_supabase_client()

        # Prepare the data
        prep_list_data = {
            "name": name,
            "company_id": company_id,
            "items": items or [],
            "status": "active"
        }

        result = supabase.table('prep_lists').insert(prep_list_data).execute()
        return {
            "success": True,
            "message": f"Created prep list '{name}'",
            "data": result.data[0] if result.data else None
        }
    except Exception as e:
        return {"error": f"Failed to create prep list: {str(e)}"}

@mcp.tool
def add_prep_item(list_id: int, item: str) -> Dict[str, Any]:
    """Add an item to an existing prep list"""
    try:
        supabase = get_supabase_client()

        # First get the current list
        current_list = supabase.table('prep_lists').select('*').eq('id', list_id).execute()

        if not current_list.data:
            return {"error": f"Prep list {list_id} not found"}

        # Update the items list
        current_items = current_list.data[0].get('items', [])
        current_items.append(item)

        result = supabase.table('prep_lists').update({
            'items': current_items
        }).eq('id', list_id).execute()

        return {
            "success": True,
            "message": f"Added '{item}' to prep list {list_id}",
            "updated_list": result.data[0] if result.data else None
        }
    except Exception as e:
        return {"error": f"Failed to add item: {str(e)}"}

@mcp.tool
def update_prep_list_status(list_id: int, status: str) -> Dict[str, Any]:
    """Update the status of a prep list (active, completed, cancelled)"""
    try:
        supabase = get_supabase_client()

        result = supabase.table('prep_lists').update({
            'status': status
        }).eq('id', list_id).execute()

        return {
            "success": True,
            "message": f"Updated prep list {list_id} status to '{status}'",
            "data": result.data[0] if result.data else None
        }
    except Exception as e:
        return {"error": f"Failed to update status: {str(e)}"}

@mcp.tool
def delete_prep_list(list_id: int) -> Dict[str, Any]:
    """Delete a prep list"""
    try:
        supabase = get_supabase_client()

        result = supabase.table('prep_lists').delete().eq('id', list_id).execute()

        return {
            "success": True,
            "message": f"Deleted prep list {list_id}",
            "deleted": result.data[0] if result.data else None
        }
    except Exception as e:
        return {"error": f"Failed to delete prep list: {str(e)}"}

# ============================================================================
# RECIPE MANAGEMENT TOOLS - If you have a recipes table
# ============================================================================

@mcp.tool
def list_recipes(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all recipes, optionally filtered by category"""
    try:
        supabase = get_supabase_client()
        query = supabase.table('recipes').select('*')

        if category:
            query = query.eq('category', category)

        result = query.execute()
        return result.data
    except Exception as e:
        return [{"error": f"Failed to fetch recipes: {str(e)}"}]

@mcp.tool
def get_recipe(recipe_id: int) -> Dict[str, Any]:
    """Get a specific recipe by ID"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('recipes').select('*').eq('id', recipe_id).execute()

        if result.data:
            return result.data[0]
        else:
            return {"error": f"Recipe {recipe_id} not found"}
    except Exception as e:
        return {"error": f"Failed to fetch recipe: {str(e)}"}

@mcp.tool
def create_recipe(name: str, ingredients: List[str], instructions: str,
                 prep_time: int, category: str = "General") -> Dict[str, Any]:
    """Create a new recipe"""
    try:
        supabase = get_supabase_client()

        recipe_data = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "prep_time": prep_time,
            "category": category
        }

        result = supabase.table('recipes').insert(recipe_data).execute()

        return {
            "success": True,
            "message": f"Created recipe '{name}'",
            "data": result.data[0] if result.data else None
        }
    except Exception as e:
        return {"error": f"Failed to create recipe: {str(e)}"}

# ============================================================================
# INVENTORY MANAGEMENT TOOLS - If you have an inventory table
# ============================================================================

@mcp.tool
def check_inventory() -> List[Dict[str, Any]]:
    """Check current inventory levels"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('inventory').select('*').execute()
        return result.data
    except Exception as e:
        return [{"error": f"Failed to fetch inventory: {str(e)}"}]

@mcp.tool
def update_inventory_item(item_name: str, quantity: int, unit: str = "pieces") -> Dict[str, Any]:
    """Update inventory quantity for an item"""
    try:
        supabase = get_supabase_client()

        result = supabase.table('inventory').upsert({
            'item_name': item_name,
            'quantity': quantity,
            'unit': unit,
            'last_updated': 'now()'
        }).execute()

        return {
            "success": True,
            "message": f"Updated {item_name} to {quantity} {unit}",
            "data": result.data[0] if result.data else None
        }
    except Exception as e:
        return {"error": f"Failed to update inventory: {str(e)}"}

# ============================================================================
# STAFF MANAGEMENT TOOLS - If you have a staff table
# ============================================================================

@mcp.tool
def list_staff() -> List[Dict[str, Any]]:
    """List all kitchen staff"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('staff').select('*').execute()
        return result.data
    except Exception as e:
        return [{"error": f"Failed to fetch staff: {str(e)}"}]

@mcp.tool
def assign_staff_to_prep_list(staff_id: int, prep_list_id: int) -> Dict[str, Any]:
    """Assign a staff member to work on a prep list"""
    try:
        supabase = get_supabase_client()

        # This assumes you have a staff_assignments table
        # Adjust table name and structure as needed
        result = supabase.table('staff_assignments').insert({
            'staff_id': staff_id,
            'prep_list_id': prep_list_id,
            'assigned_at': 'now()'
        }).execute()

        return {
            "success": True,
            "message": f"Assigned staff {staff_id} to prep list {prep_list_id}",
            "data": result.data[0] if result.data else None
        }
    except Exception as e:
        return {"error": f"Failed to assign staff: {str(e)}"}

# ============================================================================
# ANALYTICS TOOLS
# ============================================================================

@mcp.tool
def get_prep_stats(company_id: str) -> Dict[str, Any]:
    """Get prep statistics for a company"""
    try:
        supabase = get_supabase_client()

        # Count prep lists by status
        stats = {}

        # Total prep lists
        total = supabase.table('prep_lists').select('*', count='exact').eq('company_id', company_id).execute()
        stats['total_prep_lists'] = total.count

        # By status
        statuses = ['active', 'completed', 'cancelled']
        for status in statuses:
            count = supabase.table('prep_lists').select('*', count='exact').eq('company_id', company_id).eq('status', status).execute()
            stats[f'{status}_lists'] = count.count

        # Recent activity (last 7 days)
        recent = supabase.table('prep_lists').select('*', count='exact').eq('company_id', company_id).gte('created_at', 'now() - interval 7 day').execute()
        stats['recent_lists'] = recent.count

        return stats

    except Exception as e:
        return {"error": f"Failed to get stats: {str(e)}"}

# ============================================================================
# UTILITY TOOLS
# ============================================================================

@mcp.tool
def get_database_schema() -> Dict[str, Any]:
    """Get information about available database tables and their structure"""
    try:
        supabase = get_supabase_client()

        # This is a simplified schema - in a real app you'd query the database schema
        tables_info = {
            "prep_lists": {
                "description": "Kitchen prep lists and tasks",
                "columns": ["id", "name", "company_id", "items", "status", "created_at"]
            },
            "recipes": {
                "description": "Recipe definitions and instructions",
                "columns": ["id", "name", "ingredients", "instructions", "prep_time", "category"]
            },
            "inventory": {
                "description": "Kitchen inventory and stock levels",
                "columns": ["id", "item_name", "quantity", "unit", "last_updated"]
            },
            "staff": {
                "description": "Kitchen staff information",
                "columns": ["id", "name", "role", "shift", "contact_info"]
            }
        }

        return {
            "tables": tables_info,
            "note": "This is a template - customize table names and columns for your actual database"
        }

    except Exception as e:
        return {"error": f"Failed to get schema: {str(e)}"}

@mcp.tool
def test_database_connection() -> Dict[str, Any]:
    """Test the Supabase database connection"""
    try:
        supabase = get_supabase_client()

        # Try a simple query to test connection
        result = supabase.table('prep_lists').select('count', count='exact').limit(1).execute()

        return {
            "success": True,
            "message": "Database connection successful",
            "connection_info": {
                "url": SUPABASE_URL,
                "has_anon_key": bool(SUPABASE_ANON_KEY),
                "prep_lists_count": result.count if hasattr(result, 'count') else 'unknown'
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Database connection failed: {str(e)}",
            "troubleshooting": [
                "Check SUPABASE_URL environment variable",
                "Check SUPABASE_ANON_KEY environment variable",
                "Verify your Supabase project is active",
                "Check your network connection"
            ]
        }

@mcp.tool
def debug_env_vars() -> Dict[str, Any]:
    """Debug environment variables"""
    import os
    return {
        "SUPABASE_URL_exists": "SUPABASE_URL" in os.environ,
        "SUPABASE_ANON_KEY_exists": "SUPABASE_ANON_KEY" in os.environ,
        "SUPABASE_URL_value": os.getenv("SUPABASE_URL", "NOT_SET")[:50] + "...",
        "SUPABASE_ANON_KEY_value": os.getenv("SUPABASE_ANON_KEY", "NOT_SET")[:50] + "...",
        "all_env_vars": [k for k in os.environ.keys() if "SUPABASE" in k],
        "fallback_url": SUPABASE_URL[:50] + "...",
        "fallback_key": SUPABASE_ANON_KEY[:50] + "..."
    }

# ============================================================================
# PROMPTS - Reusable message templates for kitchen guidance
# ============================================================================

# Complex prompts - commented out for now
# @mcp.prompt
# def recipe_analysis(recipe_name: str, analysis_type: str = "summary") -> str:
#     """Generate a prompt for analyzing a recipe."""
#     return f"Please analyze the '{recipe_name}' recipe. Focus on: {analysis_type}."

# ============================================================================
# START THE SERVER
# ============================================================================

if __name__ == "__main__":
    print("🍳 Starting Prep Chef Database MCP Server...")
    print("=" * 50)

    # Test database connection on startup
    try:
        client = get_supabase_client()
        print("✅ Supabase connection successful")
        print("📊 Ready to serve your database tools!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Make sure SUPABASE_URL and SUPABASE_ANON_KEY are set")

    print("\n🚀 Starting MCP server...")
    mcp.run()