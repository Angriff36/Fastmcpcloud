[33mcommit c134a53f5e521b5004564338677c91b4fbfeaa14[m
Author: Angriff36 <unashamed366@gmail.com>
Date:   Fri Sep 5 16:24:57 2025 -0700

    Add Prep Chef FastMCP server files for auto-deployment
    
    - fastmcp.json: Cloud deployment configuration
    - real_supabase_server.py: Main FastMCP server with Supabase integration
    - kitchen_automations.py: Kitchen automation tools
    - prep_chef_automations/: Packaged automation library
    - test_client.py: Client for testing server functionality
    - app_integration.py: Application integration examples
    - requirements.txt & setup.py: Dependencies and packaging
    - prep-chef-mcp-config.json: MCP configuration
    
    Auto-deployment system can now access all necessary files.

app_integration.py
fastmcp.json
kitchen_automations.py
prep-chef-mcp-config.json
prep_chef_automations/__init__.py
prep_chef_automations/kitchen_automations.py
real_supabase_server.py
real_supabase_server_simple.py
requirements.txt
setup.py
test_client.py
