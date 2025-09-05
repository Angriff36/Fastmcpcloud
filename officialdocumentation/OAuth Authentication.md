---
title: "OAuth Authentication"
source: "https://gofastmcp.com/clients/auth/oauth"
author:
  - "[[FastMCP]]"
published:
created: 2025-09-04
description: "Authenticate your FastMCP client via OAuth 2.1."
tags:
  - "clippings"
---
`` New in version: `2.6.0` ``

OAuth authentication is only relevant for HTTP-based transports and requires user interaction via a web browser.

When your FastMCP client needs to access an MCP server protected by OAuth 2.1, and the process requires user interaction (like logging in and granting consent), you should use the Authorization Code Flow. FastMCP provides the `fastmcp.client.auth.OAuth` helper to simplify this entire process.This flow is common for user-facing applications where the application acts on behalf of the user.

## Client Usage

### Default Configuration

The simplest way to use OAuth is to pass the string `"oauth"` to the `auth` parameter of the `Client` or transport instance. FastMCP will automatically configure the client to use OAuth with default settings:

```
from fastmcp import Client

# Uses default OAuth settings

async with Client("https://fastmcp.cloud/mcp", auth="oauth") as client:

    await client.ping()
```

### OAuth Helper

To fully configure the OAuth flow, use the `OAuth` helper and pass it to the `auth` parameter of the `Client` or transport instance. `OAuth` manages the complexities of the OAuth 2.1 Authorization Code Grant with PKCE (Proof Key for Code Exchange) for enhanced security, and implements the full `httpx.Auth` interface.

```
from fastmcp import Client

from fastmcp.client.auth import OAuth

oauth = OAuth(mcp_url="https://fastmcp.cloud/mcp")

async with Client("https://fastmcp.cloud/mcp", auth=oauth) as client:

    await client.ping()
```

#### OAuth Parameters

- **`mcp_url`** (`str`): The full URL of the target MCP server endpoint. Used to discover OAuth server metadata
- **`scopes`** (`str | list[str]`, optional): OAuth scopes to request. Can be space-separated string or list of strings
- **`client_name`** (`str`, optional): Client name for dynamic registration. Defaults to `"FastMCP Client"`
- **`token_storage_cache_dir`** (`Path`, optional): Token cache directory. Defaults to `~/.fastmcp/oauth-mcp-client-cache/`
- **`additional_client_metadata`** (`dict[str, Any]`, optional): Extra metadata for client registration
- **`callback_port`** (`int`, optional): Fixed port for OAuth callback server. If not specified, uses a random available port

## OAuth Flow

The OAuth flow is triggered when you use a FastMCP `Client` configured to use OAuth.

## Token Management

### Token Storage

OAuth access tokens are automatically cached in `~/.fastmcp/oauth-mcp-client-cache/` and persist between application runs. Files are keyed by the OAuth server’s base URL.

### Managing Cache

To clear the tokens for a specific server, instantiate a `FileTokenStorage` instance and call the `clear` method:

```
from fastmcp.client.auth.oauth import FileTokenStorage

storage = FileTokenStorage(server_url="https://fastmcp.cloud/mcp")

await storage.clear()
```

To clear *all* tokens for all servers, call the `clear_all` method on the `FileTokenStorage` class:

```
from fastmcp.client.auth.oauth import FileTokenStorage

FileTokenStorage.clear_all()
```