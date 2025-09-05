---
title: "Progress Monitoring"
source: "https://gofastmcp.com/clients/progress"
author:
  - "[[FastMCP]]"
published:
created: 2025-09-04
description: "Handle progress notifications from long-running server operations."
tags:
  - "clippings"
---
`` New in version: `2.3.5` `` MCP servers can report progress during long-running operations. The client can receive these updates through a progress handler.

## Progress Handler

Set a progress handler when creating the client:

```
from fastmcp import Client

async def my_progress_handler(

    progress: float, 

    total: float | None, 

    message: str | None

) -> None:

    if total is not None:

        percentage = (progress / total) * 100

        print(f"Progress: {percentage:.1f}% - {message or ''}")

    else:

        print(f"Progress: {progress} - {message or ''}")

client = Client(

    "my_mcp_server.py",

    progress_handler=my_progress_handler

)
```

### Handler Parameters

The progress handler receives three parameters:

## Progress Handler Parametersprogress

float

Current progress valuetotal

float | None

Expected total value (may be None)message

str | None

Optional status message (may be None)

## Per-Call Progress Handler

Override the progress handler for specific tool calls:

```
async with client:

    # Override with specific progress handler for this call

    result = await client.call_tool(

        "long_running_task", 

        {"param": "value"}, 

        progress_handler=my_progress_handler

    )
```