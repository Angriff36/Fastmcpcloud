---
title: "GitHub OAuth 🤝 FastMCP"
source: "https://gofastmcp.com/integrations/github"
author:
  - "[[FastMCP]]"
published:
created: 2025-09-04
description: "Secure your FastMCP server with GitHub OAuth"
tags:
  - "clippings"
---
`` New in version: `2.12.0` `` This guide shows you how to secure your FastMCP server using **GitHub OAuth**. Since GitHub doesn’t support Dynamic Client Registration, this integration uses the [**OAuth Proxy**](https://gofastmcp.com/servers/auth/oauth-proxy) pattern to bridge GitHub’s traditional OAuth with MCP’s authentication requirements.

## Configuration

### Prerequisites

Before you begin, you will need:
1. A **[GitHub Account](https://github.com/)** with access to create OAuth Apps
2. Your FastMCP server’s URL (can be localhost for development, e.g., `http://localhost:8000`)

### Step 1: Create a GitHub OAuth App

Create an OAuth App in your GitHub settings to get the credentials needed for authentication:

### Step 2: FastMCP Configuration

Create your FastMCP server using the `GitHubProvider`, which handles GitHub’s OAuth quirks automatically:

server.py

```
from fastmcp import FastMCP

from fastmcp.server.auth.providers.github import GitHubProvider

# The GitHubProvider handles GitHub's token format and validation

auth_provider = GitHubProvider(

    client_id="Ov23liAbcDefGhiJkLmN",  # Your GitHub OAuth App Client ID

    client_secret="github_pat_...",     # Your GitHub OAuth App Client Secret

    base_url="http://localhost:8000",   # Must match your OAuth App configuration

    # redirect_path="/auth/callback"   # Default value, customize if needed

)

mcp = FastMCP(name="GitHub Secured App", auth=auth_provider)

# Add a protected tool to test authentication

@mcp.tool

async def get_user_info() -> dict:

    """Returns information about the authenticated GitHub user."""

    from fastmcp.server.dependencies import get_access_token

    

    token = get_access_token()

    # The GitHubProvider stores user data in token claims

    return {

        "github_user": token.claims.get("login"),

        "name": token.claims.get("name"),

        "email": token.claims.get("email")

    }
```

## Testing

### Running the Server

Start your FastMCP server with HTTP transport to enable OAuth flows:

```
fastmcp run server.py --transport http --port 8000
```

Your server is now running and protected by GitHub OAuth authentication.

### Testing with a Client

Create a test client that authenticates with your GitHub-protected server:When you run the client for the first time:
1. Your browser will open to GitHub’s authorization page
2. After you authorize the app, you’ll be redirected back
3. The client receives the token and can make authenticated requests

The client caches tokens locally, so you won’t need to re-authenticate for subsequent runs unless the token expires or you explicitly clear the cache.

## Environment Variables

`` New in version: `2.12.1` `` For production deployments, use environment variables instead of hardcoding credentials.

### Provider Selection

Setting this environment variable allows the GitHub provider to be used automatically without explicitly instantiating it in code.FASTMCP\_SERVER\_AUTH

default:"Not set"

Set to `fastmcp.server.auth.providers.github.GitHubProvider` to use GitHub authentication.

### GitHub-Specific Configuration

These environment variables provide default values for the GitHub provider, whether it’s instantiated manually or configured via `FASTMCP_SERVER_AUTH`.FASTMCP\_SERVER\_AUTH\_GITHUB\_CLIENT\_ID

required

Your GitHub OAuth App Client ID (e.g., `Ov23liAbcDefGhiJkLmN`)FASTMCP\_SERVER\_AUTH\_GITHUB\_CLIENT\_SECRET

required

Your GitHub OAuth App Client SecretFASTMCP\_SERVER\_AUTH\_GITHUB\_BASE\_URL

default:"http://localhost:8000"

Public URL of your FastMCP server for OAuth callbacksFASTMCP\_SERVER\_AUTH\_GITHUB\_REDIRECT\_PATH

default:"/auth/callback"

Redirect path configured in your GitHub OAuth AppFASTMCP\_SERVER\_AUTH\_GITHUB\_REQUIRED\_SCOPES

default:"\[\\"user\\"\]"

Comma-, space-, or JSON-separated list of required GitHub scopes (e.g., `user repo` or `["user","repo"]`)FASTMCP\_SERVER\_AUTH\_GITHUB\_TIMEOUT\_SECONDS

default:"10"

HTTP request timeout for GitHub API calls

Example `.env` file:

```
# Use the GitHub provider

FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.github.GitHubProvider

# GitHub OAuth credentials

FASTMCP_SERVER_AUTH_GITHUB_CLIENT_ID=Ov23liAbcDefGhiJkLmN

FASTMCP_SERVER_AUTH_GITHUB_CLIENT_SECRET=github_pat_...

FASTMCP_SERVER_AUTH_GITHUB_BASE_URL=https://your-server.com

FASTMCP_SERVER_AUTH_GITHUB_REQUIRED_SCOPES=user,repo
```

With environment variables set, your server code simplifies to:

server.py

```
from fastmcp import FastMCP

# Authentication is automatically configured from environment

mcp = FastMCP(name="GitHub Secured App")

@mcp.tool

async def list_repos() -> list[str]:

    """List the authenticated user's repositories."""

    # Your tool implementation here

    pass
```