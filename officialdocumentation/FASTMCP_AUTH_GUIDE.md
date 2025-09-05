# FastMCP Authentication Guide for Prep Chef

## Understanding FastMCP

FastMCP is a **framework** for building MCP (Model Context Protocol) servers, not a hosted service. When you see URLs like `https://horrible-wasp.fastmcp.app/mcp`, that's **FastMCP Cloud** - a hosting service for FastMCP servers.

## Key Concepts

### 1. **You Create the Server**
- FastMCP is a Python library for building servers
- You define tools, resources, and authentication rules
- You deploy and run the server yourself (or use FastMCP Cloud)

### 2. **Authentication is Optional and Configurable**
- **Development**: No auth needed
- **Production**: You implement the auth pattern you want
- **Tokens**: You create and manage your own API keys/tokens

### 3. **FastMCP Doesn't Issue API Keys**
- FastMCP validates tokens you provide
- You decide what tokens are valid
- You can integrate with external auth providers

## Quick Start: Your Own FastMCP Server

### Step 1: Run the Demo Server
```bash
# Install FastMCP if not already installed
pip install fastmcp

# Run our demo server
python simple_fastmcp_server.py
```

### Step 2: Test Your Server
```bash
# In another terminal, test the servers
python test_own_fastmcp.py
```

## Authentication Patterns

### Pattern 1: No Authentication (Development)
```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def my_tool() -> str:
    return "Hello from unauthenticated server!"

# Run: mcp.run(transport="http", port=8000)
# Access: http://localhost:8000/mcp
```

### Pattern 2: Static Token Authentication
```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

# Define your API tokens
tokens = {
    "my-secret-token-123": {
        "client_id": "prep-chef-app",
        "scopes": ["read:data", "write:data"]
    }
}

auth = StaticTokenVerifier(tokens=tokens)
mcp = FastMCP("My Secure Server", auth=auth)

@mcp.tool
def secure_tool() -> str:
    return "Hello from authenticated server!"
```

**Usage:**
```bash
curl -H "Authorization: Bearer my-secret-token-123" http://localhost:8000/mcp
```

### Pattern 3: JWT Integration
```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier

auth = JWTVerifier(
    jwks_uri="https://your-auth-provider.com/.well-known/jwks.json",
    issuer="https://your-auth-provider.com",
    audience="your-app-id"
)

mcp = FastMCP("JWT Server", auth=auth)
```

### Pattern 4: OAuth Integration
```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.workos import AuthKitProvider

auth = AuthKitProvider(
    authkit_domain="https://your-project.authkit.app",
    base_url="https://your-server.com"
)

mcp = FastMCP("OAuth Server", auth=auth)
```

## For Your Prep Chef Project

### Recommended Approach for Development:
1. **Start with no authentication** for development
2. **Use static tokens** for basic API access
3. **Integrate with Supabase auth** later for production

### Example Integration with Supabase:
```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier

# Configure for Supabase JWT tokens
auth = JWTVerifier(
    jwks_uri="https://your-project.supabase.co/.well-known/jwks.json",
    issuer="https://your-project.supabase.co",
    audience="authenticated"
)

mcp = FastMCP("Prep Chef MCP", auth=auth)

@mcp.tool
def get_company_prep_lists(company_id: str) -> list:
    """Get prep lists for a specific company."""
    from fastmcp.server.dependencies import get_access_token
    
    token = get_access_token()
    # Extract user info from Supabase JWT
    user_id = token.claims.get("sub") if token else None
    
    # Your existing Supabase logic here
    return get_prep_lists_for_company(company_id, user_id)
```

## FastMCP Cloud Authentication

For the FastMCP Cloud server you were trying to access (`https://horrible-wasp.fastmcp.app/mcp`):

1. **Check your FastMCP Cloud dashboard** for authentication requirements
2. **Look for API keys or OAuth setup** in your account settings
3. **Consider that it might be a demo server** with specific auth requirements
4. **Create your own server instead** - it's easier to control

## Next Steps

1. **Run the demo servers** I created
2. **Test the authentication patterns**
3. **Integrate with your existing Prep Chef authentication**
4. **Deploy to production when ready**

## Troubleshooting

### "401 Unauthorized" Errors
- Server requires authentication
- Check if you're using the right token format
- Verify the token is valid for that server

### "Connection Refused" Errors  
- Server isn't running
- Wrong port or URL
- Firewall issues

### "Tool Not Found" Errors
- Server doesn't have that tool
- Check available tools with `list_tools()`
- Verify authentication for protected tools

## Resources

- **FastMCP Documentation**: https://gofastmcp.com
- **MCP Specification**: https://modelcontextprotocol.io
- **Your Demo Server**: `simple_fastmcp_server.py`
- **Test Client**: `test_own_fastmcp.py`
