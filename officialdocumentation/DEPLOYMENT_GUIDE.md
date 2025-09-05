# 🚀 Deploying Your Real Supabase MCP Server to FastMCP Cloud

## What You Have Now

✅ **FastMCP Cloud Server**: `https://horrible-wasp.fastmcp.app/mcp` (currently has demo/example tools)
✅ **Supabase Environment Variables**: Already configured in FastMCP Cloud
❌ **Real Database Tools**: Need to deploy the actual Supabase-connected server

## Files You Need

1. **`real_supabase_server.py`** - Your actual MCP server with Supabase tools
2. **`requirements.txt`** - Python dependencies
3. **Supabase Environment Variables** - Already set in FastMCP Cloud

## Step 1: Customize the Server for Your Database

### A. Update Table Names

Replace the table names in `real_supabase_server.py` with your actual Supabase table names:

```python
# Change these table names to match your Supabase database:
supabase.table('prep_lists')    # → supabase.table('your_prep_table_name')
supabase.table('recipes')       # → supabase.table('your_recipes_table_name')
supabase.table('inventory')     # → supabase.table('your_inventory_table_name')
supabase.table('staff')         # → supabase.table('your_staff_table_name')
```

### B. Update Column Names

Update the column names to match your actual database schema:

```python
# Example: If your prep_lists table has different column names
prep_list_data = {
    "name": name,                    # Keep as-is
    "company_id": company_id,       # Keep as-is
    "items": items or [],           # Keep as-is
    "status": "active",             # Keep as-is
    # Add your custom columns here
    "created_by": user_id,          # Add custom columns
    "priority": "normal",           # Add custom columns
}
```

### C. Add Your Custom Tools

Add tools specific to your business logic:

```python
@mcp.tool
def your_custom_tool(param1: str, param2: int) -> Dict[str, Any]:
    """Description of your custom tool"""
    try:
        supabase = get_supabase_client()
        # Your custom database operations here
        result = supabase.table('your_table').select('*').eq('param1', param1).execute()
        return {"data": result.data}
    except Exception as e:
        return {"error": str(e)}
```

## Step 2: Test Locally First

### A. Set Environment Variables

Create a `.env` file in your project root:

```bash
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### B. Install Dependencies

```bash
pip install -r requirements.txt
```

### C. Test the Server

```bash
python real_supabase_server.py
```

The server will start and test the Supabase connection. If it fails, check:
- Your Supabase URL and key
- Network connectivity
- Supabase project status

## Step 3: Deploy to FastMCP Cloud

### A. Push Your Code to GitHub

1. Commit your changes:
```bash
git add .
git commit -m "Add real Supabase database tools"
git push origin main
```

2. Your FastMCP Cloud server will automatically redeploy with the new code

### B. Verify Environment Variables

In your FastMCP Cloud dashboard:
1. Go to your project settings
2. Verify these environment variables are set:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`

### C. Monitor Deployment

Check your FastMCP Cloud dashboard for:
- ✅ Build status
- ✅ Deployment logs
- ✅ Server health

## Step 4: Test Your Deployed Server

### A. Use the Test Script

```bash
python simple_check.py
```

This will:
- Connect to your deployed server
- List all available tools
- Test database connectivity
- Show your actual Supabase data

### B. Test Specific Tools

Once connected, you can test tools like:
- `list_prep_lists()` - Get all prep lists
- `create_prep_list(name, company_id)` - Create new prep list
- `test_database_connection()` - Verify Supabase connection

## Available Tools After Deployment

### Core Prep List Tools:
- **`list_prep_lists(company_id?)`** - List prep lists (filter by company)
- **`get_prep_list(list_id)`** - Get specific prep list
- **`create_prep_list(name, company_id, items?)`** - Create new prep list
- **`add_prep_item(list_id, item)`** - Add item to prep list
- **`update_prep_list_status(list_id, status)`** - Update status
- **`delete_prep_list(list_id)`** - Delete prep list

### Recipe Management:
- **`list_recipes(category?)`** - List recipes (filter by category)
- **`get_recipe(recipe_id)`** - Get specific recipe
- **`create_recipe(name, ingredients, instructions, prep_time, category?)`** - Create recipe

### Inventory Management:
- **`check_inventory()`** - Check all inventory
- **`update_inventory_item(item_name, quantity, unit?)`** - Update inventory

### Staff Management:
- **`list_staff()`** - List all staff
- **`assign_staff_to_prep_list(staff_id, prep_list_id)`** - Assign staff

### Analytics:
- **`get_prep_stats(company_id)`** - Get prep statistics

### Utilities:
- **`get_database_schema()`** - Show database structure
- **`test_database_connection()`** - Test Supabase connection

## Step 5: Connect to AI Applications

### Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "prep-chef-db": {
      "command": "python",
      "args": ["-c", "import sys; print('OAuth URL needed')"],
      "env": {
        "FASTMCP_AUTH_URL": "https://horrible-wasp.fastmcp.app/mcp"
      }
    }
  }
}
```

### Test with Claude

You can now ask Claude things like:
- "Show me all active prep lists"
- "Create a new prep list for tomorrow's service"
- "What's in our current inventory?"
- "Add 'chop vegetables' to prep list #1"
- "Show me recipes in the 'Desserts' category"

## Troubleshooting

### Common Issues:

1. **"Table doesn't exist" errors**
   - Check your actual table names in Supabase
   - Update the table names in `real_supabase_server.py`

2. **"Column doesn't exist" errors**
   - Check your database schema
   - Update column names in the tools

3. **Authentication failures**
   - Verify SUPABASE_URL and SUPABASE_ANON_KEY
   - Check they're set in FastMCP Cloud environment variables

4. **Connection timeouts**
   - Check Supabase project status
   - Verify network connectivity
   - Check Supabase rate limits

### Debug Commands:

```bash
# Test local server
python real_supabase_server.py

# Test deployed server
python simple_check.py

# Check server logs
# Go to FastMCP Cloud dashboard → View server logs
```

## Next Steps

1. **Customize for your schema** - Update table/column names
2. **Add business logic** - Create tools specific to your workflow
3. **Test thoroughly** - Verify all tools work with your data
4. **Connect AI assistants** - Integrate with Claude, ChatGPT, etc.
5. **Scale up** - Add more tools as your needs grow

Your server is now a **real database-connected MCP server** that AI can use to interact with your Supabase data! 🎉


