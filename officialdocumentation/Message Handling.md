---
title: "Message Handling"
source: "https://gofastmcp.com/clients/messages"
author:
  - "[[FastMCP]]"
published:
created: 2025-09-04
description: "Handle MCP messages, requests, and notifications with custom message handlers."
tags:
  - "clippings"
---
`` New in version: `2.9.1` `` MCP clients can receive various types of messages from servers, including requests that need responses and notifications that don’t. The message handler provides a unified way to process all these messages.

## Function-Based Handler

The simplest way to handle messages is with a function that receives all messages:

```
from fastmcp import Client

async def message_handler(message):

    """Handle all MCP messages from the server."""

    if hasattr(message, 'root'):

        method = message.root.method

        print(f"Received: {method}")

        

        # Handle specific notifications

        if method == "notifications/tools/list_changed":

            print("Tools have changed - might want to refresh tool cache")

        elif method == "notifications/resources/list_changed":

            print("Resources have changed")

client = Client(

    "my_mcp_server.py",

    message_handler=message_handler,

)
```

## Message Handler Class

For fine-grained targeting, FastMCP provides a `MessageHandler` class you can subclass to take advantage of specific hooks:

```
from fastmcp import Client

from fastmcp.client.messages import MessageHandler

import mcp.types

class MyMessageHandler(MessageHandler):

    async def on_tool_list_changed(

        self, notification: mcp.types.ToolListChangedNotification

    ) -> None:

        """Handle tool list changes specifically."""

        print("Tool list changed - refreshing available tools")

client = Client(

    "my_mcp_server.py",

    message_handler=MyMessageHandler(),

)
```

### Available Handler Methods

All handler methods receive a single argument - the specific message type:

## Example: Handling Tool Changes

Here’s a practical example of handling tool list changes:

```
from fastmcp.client.messages import MessageHandler

import mcp.types

class ToolCacheHandler(MessageHandler):

    def __init__(self):

        self.cached_tools = []

    

    async def on_tool_list_changed(

        self, notification: mcp.types.ToolListChangedNotification

    ) -> None:

        """Clear tool cache when tools change."""

        print("Tools changed - clearing cache")

        self.cached_tools = []  # Force refresh on next access

client = Client("server.py", message_handler=ToolCacheHandler())
```

## Handling Requests

While the message handler receives server-initiated requests, for most use cases you should use the dedicated callback parameters instead:
- **Sampling requests**: Use [`sampling_handler`](https://gofastmcp.com/clients/sampling)
- **Progress requests**: Use [`progress_handler`](https://gofastmcp.com/clients/progress)
- **Log requests**: Use [`log_handler`](https://gofastmcp.com/clients/logging)
The message handler is primarily for monitoring and handling notifications rather than responding to requests.