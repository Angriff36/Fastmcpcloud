---
title: "Client Roots"
source: "https://gofastmcp.com/clients/roots"
author:
  - "[[FastMCP]]"
published:
created: 2025-09-04
description: "Provide local context and resource boundaries to MCP servers."
tags:
  - "clippings"
---
`` New in version: `2.0.0` `` Roots are a way for clients to inform servers about the resources they have access to. Servers can use this information to adjust behavior or provide more relevant responses.

## Setting Static Roots

Provide a list of roots when creating the client:

```
from fastmcp import Client

client = Client(

    "my_mcp_server.py", 

    roots=["/path/to/root1", "/path/to/root2"]

)
```