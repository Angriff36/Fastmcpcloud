# FastMCP Cloud Reference Guide

## What is FastMCP Cloud?
FastMCP Cloud is a hosting service that takes your MCP (Model Context Protocol) server code and runs it 24/7 on the internet. Instead of running your server locally on your computer, it runs in the cloud and gives you a permanent URL that other applications can connect to.

**Why use it?**
- Your MCP server is always available (no need to keep your computer running)
- Other people can connect to your server from anywhere
- Automatic scaling and reliability
- Easy deployment - just push code to Git and it deploys automatically

## How to Deploy Your Server to FastMCP Cloud

### 1. Configuration File (`fastmcp.json`)

**What it does:** This file tells FastMCP Cloud exactly how to run your server. Think of it as a recipe that says "Here's my code, here's what it needs to run, and here's how other apps can connect to it."

**Breaking it down:**
- **server.entrypoint**: Which Python file contains your MCP server code
- **server.transport**: How the server communicates with the outside world (HTTP on port 8000, accessible from anywhere)
- **environment**: Secret keys and settings your server needs (like database passwords)
- **dependencies**: What Python packages to install (like supabase for database access)

```json
{
  "server": {
    "entrypoint": "real_supabase_server.py",
    "transport": {
      "type": "http",
      "host": "0.0.0.0",
      "port": 8000
    }
  },
  "environment": {
    "SUPABASE_URL": "https://zdqkhjwxzkpjokcidera.supabase.co",
    "SUPABASE_ANON_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "dependencies": [
    "fastmcp>=2.0.0",
    "supabase>=2.0.0",
    "python-dotenv>=1.0.0"
  ]
}
```

### 2. Build Process (What Happens When You Deploy)

**What it does:** When you push code to Git, FastMCP Cloud automatically builds and deploys your server. Here's what happens behind the scenes:

- **Repository**: Takes your code from GitHub
- **Entrypoint Detection**: Automatically finds your MCP server code (looks for variables named `mcp`, `server`, or `app`)
- **Dependency Installation**: Installs all the Python packages your server needs from `requirements.txt` or `pyproject.toml`
- **Python Version**: Uses Python 3.12 (confirmed in our build logs)
- **Package Manager**: Uses `uv` (a fast Python package installer)
- **Build Container**: Runs everything in a secure Docker container on AWS

**Why this matters:** You don't have to worry about setting up servers or installing dependencies - the cloud does it all automatically!

### 3. Entry Point Types (How FastMCP Finds Your Server Code)

**What it does:** FastMCP needs to know which part of your code contains the server. There are different ways to tell it:

#### Inferred Server Instance (What we used)
```bash
fastmcp run server.py
```
**What it does:** Automatically searches your code for a FastMCP server (looks for variables named `mcp`, `server`, or `app`)
**Our experience:** Found our server in `echo.py` because it had `mcp = FastMCP("Prep Chef Database Server")`
**Best for:** Simple projects where you just want it to "figure it out"

#### Explicit Server Entrypoint
```bash
fastmcp run server.py:custom_name
```
**What it does:** You tell it exactly which variable name to use
**Example:** `server.py:my_server` - runs the server stored in variable `my_server`
**Best for:** When you have multiple servers in one file

#### Factory Function
```bash
fastmcp run server.py:create_server
```
**What it does:** Calls a function that creates and returns your server
**Example:** Useful if you need to run setup code before starting the server
**Best for:** Advanced setups with initialization code

#### FastMCP Configuration File
```bash
fastmcp run fastmcp.json
```
**What it does:** Uses a config file to specify everything (what we use for cloud deployment)
**Best for:** Cloud deployments and complex configurations

### 4. Transport Configuration (How Your Server Communicates)

**What it does:** Defines how your server talks to the outside world.

- **Type**: HTTP - Uses web requests (like a website)
- **Host**: 0.0.0.0 - Accepts connections from anywhere on the internet
- **Port**: 8000 inside the container, exposed as 8080 to the world

**Why this matters:** Makes your server accessible from any device with an internet connection.

### 5. Server Inspection Process (Quality Check)

**What it does:** FastMCP automatically checks your server to make sure it works correctly.

- **Command**: `fastmcp inspect -f fastmcp -o /tmp/server-info.json`
- **What it checks**: Finds all your tools and makes sure they're properly defined
- **Our result**: Found "Prep Chef Database Server" with all our database tools
- **Output**: Creates a detailed report of what your server can do

**Why this matters:** Catches problems before deployment so you know your server will work.

### 6. Deployment Results (Your Live Server)

**What happened:** Your server is now running 24/7 in the cloud!

- **Live URL**: `https://horrible-wasp.fastmcp.app/mcp` - Anyone can connect here
- **Status**: ✅ Successfully deployed and running
- **Server Tools**: All your Supabase database functions are working
- **Authentication**: Passthrough mode (lets the connecting app handle auth)
- **Billing**: Hobby tier (free tier)

**What you can do now:** Connect MCP clients like Claude Desktop to your server URL!

### 7. Database Tools Available (What Your Server Can Do)

**Your Prep Chef server provides these kitchen management tools:**

- `list_prep_lists()` - See all your prep lists
- `get_prep_list()` - Get details for a specific prep list
- `create_prep_list()` - Make a new prep list
- `add_prep_item()` - Add items to an existing prep list
- `update_prep_list_status()` - Change list status (active, completed, cancelled)
- `delete_prep_list()` - Remove a prep list
- `get_prep_stats()` - Get statistics about your prep work
- **Plus:** Recipe management, inventory tracking, and staff assignments

**Real-world use:** AI assistants can now help manage your kitchen operations by connecting to this server!

### 8. Environment Variables (Configuration Settings)

**What they do:** These are like settings that your server reads to know how to connect to things:

- `SUPABASE_URL` - Where your database lives on the internet
- `SUPABASE_ANON_KEY` - Password to access your database
- `FASTMCP_CLOUD_URL` - The web address of your deployed server
- `FASTMCP_CLOUD_GIT_COMMIT_SHA` - Which version of your code is running
- `FASTMCP_CLOUD_GIT_REPO` - Link to your GitHub repository

**Security note:** Never share your `SUPABASE_ANON_KEY` with anyone!

### 9. Server Mounting (Running Multiple Servers)

**What it means:** You can run different MCP servers for different purposes:

- **Main Server**: `https://your-main-app.fastmcp.app/mcp`
- **Test Server**: `https://your-test-app.fastmcp.app/mcp`
- **Dev Server**: `https://your-dev-app.fastmcp.app/mcp`

**Benefits:**
- Test new features without breaking your main server
- Different servers for different restaurant locations
- Scale busy servers independently
- Keep development and production separate

### 10. Build Artifacts (Technical Details)

**What happens during deployment:**
- Your code gets packaged into a Docker container
- Container gets uploaded to AWS ECR (Amazon's container storage)
- Container name: `fastmcp-prd-images:horrible-wasp-deletedsoon-[commit]-latest`
- Registry location: `342547628772.dkr.ecr.us-east-1.amazonaws.com`
- Desktop Extension file (.dxt) created for easy client installation

**Why this matters:** This is the "behind the scenes" of how your server gets deployed globally.

## 11. Kitchen Automation Tools (Deterministic Business Logic)

**What it does:** Pre-built automation tools that work WITHOUT AI/LLM guidance - pure programmatic business logic for your kitchen operations.

### Kitchen Dashboard (`kitchen_automations.py`)
**Real-time status monitoring:**
- Active vs completed prep lists count
- Low stock inventory alerts
- Staff on duty count
- Completion rate analytics
- Urgent alert system

**Integration:** Perfect for web dashboards, mobile apps, or cron jobs
```python
dashboard = KitchenDashboard("http://localhost:8001/mcp")
status = await dashboard.get_status()
alerts = await dashboard.get_alerts()
```

### Recipe Scaling (`kitchen_automations.py`)
**Automatic recipe scaling for different serving sizes:**
- Proportional ingredient scaling
- Maintains recipe integrity
- Saves scaled versions to database
- Tracks original vs scaled quantities

**Integration:** Event booking systems, order management, catering software
```python
scaler = RecipeScaler("http://localhost:8001/mcp")
result = await scaler.scale_recipe("1", 75)  # Scale recipe ID 1 to 75 servings
```

### Prep List Automation (`kitchen_automations.py`)
**Generate prep lists from event bookings:**
- Auto-calculates quantities based on guest count
- Includes standard event setup items
- Creates structured prep workflows
- Links to event metadata

**Integration:** Event management systems, booking platforms, catering software
```python
automation = PrepListAutomation("http://localhost:8001/mcp")
result = await automation.generate_from_event(event_data)
```

## 12. Integration Requirements (NO AI/LLM Needed)

### ✅ What These Tools CAN Work With:
- **Webhook endpoints** - Trigger automations from booking systems
- **Cron jobs** - Daily inventory checks, cleanup tasks
- **API integrations** - Connect to POS systems, booking platforms
- **Web applications** - Real-time dashboards for kitchen staff
- **Mobile apps** - Kitchen staff can trigger automations on-the-go
- **Email/SMS alerts** - Automated notifications for critical events
- **IoT sensors** - Temperature monitoring, inventory tracking
- **Existing business software** - ERP systems, accounting software

### ✅ What These Tools DON'T Need:
- ❌ **NO AI/LLM required** - Pure deterministic business logic
- ❌ **NO complex ML models** - Simple math and data processing
- ❌ **NO natural language processing** - Structured data only
- ❌ **NO autonomous agents** - Explicit, controlled operations

### 🚀 **Real-World Integration Examples:**

1. **Event Booking System Integration:**
   ```python
   # When new event is booked
   @app.route('/webhook/event-booked')
   async def handle_new_event():
       automation = PrepListAutomation()
       await automation.generate_from_event(request.json)
   ```

2. **Daily Kitchen Dashboard:**
   ```bash
   # Cron job every morning
   0 6 * * * python -c "from kitchen_automations import KitchenDashboard; import asyncio; asyncio.run(KitchenDashboard().send_daily_report())"
   ```

3. **Inventory Alert System:**
   ```python
   # Check inventory every hour
   while True:
       dashboard = KitchenDashboard()
       alerts = await dashboard.get_alerts()
       if alerts:
           send_alerts_to_management(alerts)
       await asyncio.sleep(3600)  # Wait 1 hour
   ```

## 13. MCP JSON Configuration Generation (For Desktop Apps)

**What it does:** Creates configuration files so you can connect MCP-compatible apps (like Claude Desktop, Cursor, VS Code) to your server.

**Why you'd use this:** Instead of using the cloud URL, you can run your server locally and connect desktop apps directly to it.

### Basic MCP JSON Generation
```bash
fastmcp install mcp-json real_supabase_server.py
```

**What this does:** Creates a simple config that tells desktop apps how to start your server.

**Output:**
```json
{
  "Prep Chef Database Server": {
    "command": "fastmcp",
    "args": [
      "run",
      "C:\\Projects\\Prep\\ChefPrepBoltDownload\\project\\fastmcp\\FastMCPCloud\\fastmcp-quickstart-20250904-uf9r\\real_supabase_server.py"
    ]
  }
}
```

### MCP JSON with Environment Variables and Dependencies

```bash
fastmcp install mcp-json real_supabase_server.py --env SUPABASE_URL=<url> --env SUPABASE_ANON_KEY=<key> --with supabase
```

**What this does:** Includes your database secrets and required packages in the config.

**Output:**
```json
{
  "Prep Chef Database Server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "supabase",
      "fastmcp",
      "run",
      "/path/to/real_supabase_server.py"
    ],
    "env": {
      "SUPABASE_URL": "https://...",
      "SUPABASE_ANON_KEY": "eyJ..."
    }
  }
}
```

### MCP JSON with Requirements File

```bash
fastmcp install mcp-json real_supabase_server.py --with-requirements requirements.txt
```

**What this does:** Uses your requirements.txt file to install all needed packages.

### MCP JSON with Specific Python Version

```bash
fastmcp install mcp-json real_supabase_server.py --python 3.11 --name "Prep Chef v3.11"
```

**What this does:** Forces the server to run on Python 3.11 instead of the system default.

### MCP JSON with Clipboard Copy

```bash
fastmcp install mcp-json real_supabase_server.py --copy
```

**What this does:** Copies the configuration to your clipboard for easy pasting.
**Output:** "MCP configuration for 'Prep Chef Database Server' copied to clipboard"

### Save MCP JSON to File

```bash
fastmcp install mcp-json real_supabase_server.py > prep-chef-mcp-config.json
```

**What this does:** Saves the configuration to a file you can use with MCP clients.

### MCP Client Integration (How to Use the Config)

**Where to put the configuration:**

- **Claude Desktop**: Add to `~/.claude/claude_desktop_config.json`
- **Cursor**: Add to `~/.cursor/mcp.json`
- **VS Code**: Add to your project's `.vscode/mcp.json`
- **Any MCP-compatible app**: Look for MCP configuration settings

**What happens:** Desktop apps will be able to start your server locally and use all your kitchen management tools!

---

## Quick Start Summary

**Your server is live at:** `https://horrible-wasp.fastmcp.app/mcp`

**To connect MCP clients:**
1. **Cloud method**: Use the URL above
2. **Local method**: Generate MCP JSON config and add to your desktop app settings

**Last Updated**: Based on successful deployment of commit `7a984ca7` + MCP JSON testing + Automation Tools
**Status**: ✅ Production Ready + MCP JSON Config Tested + Automation Tools Working
**Reference Style**: Human-readable explanations added for accessibility
**Key Files**:
- `kitchen_automations.py` - Ready-to-use business logic tools
- `app_integration.py` - FastAPI example for connecting to your app
- `integration_guide.py` - Multiple integration patterns for different app architectures
