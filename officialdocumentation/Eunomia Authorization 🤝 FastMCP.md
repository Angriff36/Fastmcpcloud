---
title: "Eunomia Authorization 🤝 FastMCP"
source: "https://gofastmcp.com/integrations/eunomia-authorization"
author:
  - "[[Eunomia Auth]]"
  - "[[Add Authorization to Your Server]]"
  - "[[Create a Server with Authorization]]"
  - "[[​]]"
published:
created: 2025-09-04
description: "Add policy-based authorization to your FastMCP servers with Eunomia"
tags:
  - "clippings"
---
Add **policy-based authorization** to your FastMCP servers with one-line code addition with the **[Eunomia](https://github.com/whataboutyou-ai/eunomia) authorization middleware**.Control which tools, resources and prompts MCP clients can view and execute on your server. Define dynamic JSON-based policies and obtain a comprehensive audit log of all access attempts and violations.

## How it Works

Exploiting FastMCP’s [Middleware](https://gofastmcp.com/servers/middleware), the Eunomia middleware intercepts all MCP requests to your server and automatically maps MCP methods to authorization checks.

### Listing Operations

The middleware behaves as a filter for listing operations (`tools/list`, `resources/list`, `prompts/list`), hiding to the client components that are not authorized by the defined policies.

### Execution Operations

The middleware behaves as a firewall for execution operations (`tools/call`, `resources/read`, `prompts/get`), blocking operations that are not authorized by the defined policies.

## Add Authorization to Your Server

Eunomia is an AI-specific authorization server that handles policy decisions. The server runs embedded within your MCP server by default for a zero-effort configuration, but can alternatively be run remotely for centralized policy decisions.

### Create a Server with Authorization

First, install the `eunomia-mcp` package:

```
pip install eunomia-mcp
```

Then create a FastMCP server and add the Eunomia middleware in one line:

server.py

```
from fastmcp import FastMCP

from eunomia_mcp import create_eunomia_middleware

# Create your FastMCP server

mcp = FastMCP("Secure MCP Server 🔒")

@mcp.tool()

def add(a: int, b: int) -> int:

    """Add two numbers"""

    return a + b

# Add middleware to your server

middleware = create_eunomia_middleware(policy_file="mcp_policies.json")

mcp.add_middleware(middleware)

if __name__ == "__main__":

    mcp.run()
```

### Configure Access Policies

Use the `eunomia-mcp` CLI in your terminal to manage your authorization policies:

```
# Create a default policy file

eunomia-mcp init

# Or create a policy file customized for your FastMCP server

eunomia-mcp init --custom-mcp "app.server:mcp"
```

This creates `mcp_policies.json` file that you can further edit to your access control needs.

```
# Once edited, validate your policy file

eunomia-mcp validate mcp_policies.json
```

### Run the Server

Start your FastMCP server normally:

```
python server.py
```

The middleware will now intercept all MCP requests and check them against your policies. Requests include agent identification through headers like `X-Agent-ID`, `X-User-ID`, `User-Agent`, or `Authorization` and an automatic mapping of MCP methods to authorization resources and actions.

For detailed policy configuration, custom authentication, and remote deployments, visit the [Eunomia MCP Middleware repository](https://github.com/whataboutyou-ai/eunomia/tree/main/pkgs/extensions/mcp).