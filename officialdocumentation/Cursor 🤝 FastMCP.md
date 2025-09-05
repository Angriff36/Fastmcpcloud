---
title: "Cursor 🤝 FastMCP"
source: "https://gofastmcp.com/integrations/cursor"
author:
  - "[[Eunomia Auth]]"
published:
created: 2025-09-04
description: "Install and use FastMCP servers in Cursor"
tags:
  - "clippings"
---
**This integration focuses on running local FastMCP server files with STDIO transport.** For remote servers running with HTTP or SSE transport, use your client's native configuration - FastMCP's integrations focus on simplifying the complex local setup with dependencies and `uv` commands.

Cursor supports MCP servers through multiple transport methods including STDIO, SSE, and Streamable HTTP, allowing you to extend Cursor’s AI assistant with custom tools, resources, and prompts from your FastMCP servers.

## Requirements

This integration uses STDIO transport to run your FastMCP server locally. For remote deployments, you can run your FastMCP server with HTTP or SSE transport and configure it directly in Cursor’s settings.

## Create a Server

The examples in this guide will use the following simple dice-rolling server, saved as `server.py`.

server.py

```
import random

from fastmcp import FastMCP

mcp = FastMCP(name="Dice Roller")

@mcp.tool

def roll_dice(n_dice: int) -> list[int]:

    """Roll \`n_dice\` 6-sided dice and return the results."""

    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":

    mcp.run()
```

## Install the Server

### FastMCP CLI

`` New in version: `2.10.3` `` The easiest way to install a FastMCP server in Cursor is using the `fastmcp install cursor` command. This automatically handles the configuration, dependency management, and opens Cursor with a deeplink to install the server.

```
fastmcp install cursor server.py
```

#### Workspace Installation

`` New in version: `2.12.0` `` By default, FastMCP installs servers globally for Cursor. You can also install servers to project-specific workspaces using the `--workspace` flag:

```
# Install to current directory's .cursor/ folder

fastmcp install cursor server.py --workspace .

# Install to specific workspace

fastmcp install cursor server.py --workspace /path/to/project
```

This creates a `.cursor/mcp.json` configuration file in the specified workspace directory, allowing different projects to have their own MCP server configurations.The install command supports the same `file.py:object` notation as the `run` command. If no object is specified, it will automatically look for a FastMCP server object named `mcp`, `server`, or `app` in your file:

```
# These are equivalent if your server object is named 'mcp'

fastmcp install cursor server.py

fastmcp install cursor server.py:mcp

# Use explicit object name if your server has a different name

fastmcp install cursor server.py:my_custom_server
```

After running the command, Cursor will open automatically and prompt you to install the server. The command will be `uv`, which is expected as this is a Python STDIO server. Click “Install” to confirm:![Cursor install prompt](https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/integrations/cursor-install-mcp.png?w=280&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=32e45ab0cb22dc2ff073a2369ea65ed7)

Cursor install prompt

#### Dependencies

FastMCP offers multiple ways to manage dependencies for your Cursor servers:**Individual packages**: Use the `--with` flag to specify packages your server needs. You can use this flag multiple times:

```
fastmcp install cursor server.py --with pandas --with requests
```

**Requirements file**: For projects with a `requirements.txt` file, use `--with-requirements` to install all dependencies at once:

```
fastmcp install cursor server.py --with-requirements requirements.txt
```

**Editable packages**: When developing local packages, use `--with-editable` to install them in editable mode:

```
fastmcp install cursor server.py --with-editable ./my-local-package
```

Alternatively, you can use a `fastmcp.json` configuration file (recommended):

fastmcp.json

```
{

  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",

  "source": {

    "path": "server.py",

    "entrypoint": "mcp"

  },

  "environment": {

    "dependencies": ["pandas", "requests"]

  }

}
```

#### Python Version and Project Configuration

Control your server’s Python environment with these options:**Python version**: Use `--python` to specify which Python version your server should use. This is essential when your server requires specific Python features:

```
fastmcp install cursor server.py --python 3.11
```

**Project directory**: Use `--project` to run your server within a specific project context. This ensures `uv` discovers all project configuration files and uses the correct virtual environment:

```
fastmcp install cursor server.py --project /path/to/my-project
```

#### Environment Variables

Cursor runs servers in a completely isolated environment with no access to your shell environment or locally installed applications. You must explicitly pass any environment variables your server needs.

If your server needs environment variables (like API keys), you must include them:

```
fastmcp install cursor server.py --server-name "Weather Server" \

  --env API_KEY=your-api-key \

  --env DEBUG=true
```

Or load them from a `.env` file:

```
fastmcp install cursor server.py --server-name "Weather Server" --env-file .env
```

**`uv` must be installed and available in your system PATH**. Cursor runs in its own isolated environment and needs `uv` to manage dependencies.

### Generate MCP JSON

**Use the first-class integration above for the best experience.** The MCP JSON generation is useful for advanced use cases, manual configuration, or integration with other tools.

You can generate MCP JSON configuration for manual use:

```
# Generate configuration and output to stdout

fastmcp install mcp-json server.py --server-name "Dice Roller" --with pandas

# Copy configuration to clipboard for easy pasting

fastmcp install mcp-json server.py --server-name "Dice Roller" --copy
```

This generates the standard `mcpServers` configuration format that can be used with any MCP-compatible client.

### Manual Configuration

For more control over the configuration, you can manually edit Cursor’s configuration file. The configuration file is located at:
- **All platforms**: `~/.cursor/mcp.json`
The configuration file is a JSON object with a `mcpServers` key, which contains the configuration for each MCP server.

```
{

  "mcpServers": {

    "dice-roller": {

      "command": "python",

      "args": ["path/to/your/server.py"]

    }

  }

}
```

After updating the configuration file, your server should be available in Cursor.

#### Dependencies

If your server has dependencies, you can use `uv` or another package manager to set up the environment.When manually configuring dependencies, the recommended approach is to use `uv` with FastMCP. The configuration should use `uv run` to create an isolated environment with your specified packages:

```
{

  "mcpServers": {

    "dice-roller": {

      "command": "uv",

      "args": [

        "run",

        "--with", "fastmcp",

        "--with", "pandas",

        "--with", "requests", 

        "fastmcp",

        "run",

        "path/to/your/server.py"

      ]

    }

  }

}
```

You can also manually specify Python versions and project directories in your configuration:

```
{

  "mcpServers": {

    "dice-roller": {

      "command": "uv",

      "args": [

        "run",

        "--python", "3.11",

        "--project", "/path/to/project",

        "--with", "fastmcp",

        "fastmcp",

        "run",

        "path/to/your/server.py"

      ]

    }

  }

}
```

Note that the order of arguments is important: Python version and project settings should come before package specifications.

**`uv` must be installed and available in your system PATH**. Cursor runs in its own isolated environment and needs `uv` to manage dependencies.

#### Environment Variables

You can also specify environment variables in the configuration:

```
{

  "mcpServers": {

    "weather-server": {

      "command": "python",

      "args": ["path/to/weather_server.py"],

      "env": {

        "API_KEY": "your-api-key",

        "DEBUG": "true"

      }

    }

  }

}
```

Cursor runs servers in a completely isolated environment with no access to your shell environment or locally installed applications. You must explicitly pass any environment variables your server needs.

## Using the Server

Once your server is installed, you can start using your FastMCP server with Cursor’s AI assistant.Try asking Cursor something like:

> “Roll some dice for me”

Cursor will automatically detect your `roll_dice` tool and use it to fulfill your request, returning something like:

> 🎲 Here are your dice rolls: 4, 6, 4 You rolled 3 dice with a total of 14! The 6 was a nice high roll there!

The AI assistant can now access all the tools, resources, and prompts you’ve defined in your FastMCP server.