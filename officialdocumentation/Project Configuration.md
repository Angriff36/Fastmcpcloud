---
title: "Project Configuration"
source: "https://gofastmcp.com/deployment/server-configuration"
author:
  - "[[FastMCP]]"
published:
created: 2025-09-04
description: "Use fastmcp.json for portable, declarative project configuration"
tags:
  - "clippings"
---
`` New in version: `2.12.0` `` FastMCP supports declarative configuration through `fastmcp.json` files. This is the canonical and preferred way to configure FastMCP projects, providing a single source of truth for server settings, dependencies, and deployment options that replaces complex command-line arguments.The `fastmcp.json` file is designed to be a portable description of your server configuration that can be shared across environments and teams. When running from a `fastmcp.json` file, you can override any configuration values using CLI arguments.

## Overview

The `fastmcp.json` configuration file allows you to define all aspects of your FastMCP server in a structured, shareable format. Instead of remembering command-line arguments or writing shell scripts, you declare your server’s configuration once and use it everywhere.When you have a `fastmcp.json` file, running your server becomes as simple as:

```
# Run the server using the configuration

fastmcp run fastmcp.json

# Or if fastmcp.json exists in the current directory

fastmcp run
```

This configuration approach ensures reproducible deployments across different environments, from local development to production servers. It works seamlessly with Claude Desktop, VS Code extensions, and any MCP-compatible client.

## File Structure

The `fastmcp.json` configuration answers three fundamental questions about your server:
- **Source** = WHERE does your server code live?
- **Environment** = WHAT environment setup does it require?
- **Deployment** = HOW should the server run?
This conceptual model helps you understand the purpose of each configuration section and organize your settings effectively. The configuration file maps directly to these three concerns:

```
{

  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",

  "source": {

    // WHERE: Location of your server code

    "type": "filesystem",  // Optional, defaults to "filesystem"

    "path": "server.py",

    "entrypoint": "mcp"

  },

  "environment": {

    // WHAT: Environment setup and dependencies

    "type": "uv",  // Optional, defaults to "uv"

    "python": ">=3.10",

    "dependencies": ["pandas", "numpy"]

  },

  "deployment": {

    // HOW: Runtime configuration

    "transport": "stdio",

    "log_level": "INFO"

  }

}
```

Only the `source` field is required. The `environment` and `deployment` sections are optional and provide additional configuration when needed.

### JSON Schema Support

FastMCP provides JSON schemas for IDE autocomplete and validation. Add the schema reference to your `fastmcp.json` for enhanced developer experience:

```
{

  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",

  "source": {

    "path": "server.py",

    "entrypoint": "mcp"

  }

}
```

Two schema URLs are available:
- **Version-specific**: `https://gofastmcp.com/public/schemas/fastmcp.json/v1.json`
- **Latest version**: `https://gofastmcp.com/public/schemas/fastmcp.json/latest.json`
Modern IDEs like VS Code will automatically provide autocomplete suggestions, validation, and inline documentation when the schema is specified.

### Source Configuration

The source configuration determines **WHERE** your server code lives. It tells FastMCP how to find and load your server, whether it’s a local Python file, a remote repository, or hosted in the cloud. This section is required and forms the foundation of your configuration.

## Sourcesource

object

required

The server source configuration that determines where your server code lives.type

string

default:"filesystem"

The source type identifier that determines which implementation to use. Currently supports `"filesystem"` for local files. Future releases will add support for `"git"` and `"cloud"` source types.

ShowFileSystemSource

When `type` is `"filesystem"` (or omitted), the source points to a local Python file containing your FastMCP server:path

string

required

Path to the Python file containing your FastMCP server.entrypoint

string

Name of the server instance or factory function within the module:
- Can be a FastMCP server instance (e.g., `mcp = FastMCP("MyServer")`)
- Can be a function with no arguments that returns a FastMCP server
- If not specified, FastMCP searches for common names: `mcp`, `server`, or `app`

**Example:**

```
"source": {

  "type": "filesystem",

  "path": "src/server.py",

  "entrypoint": "mcp"

}
```

Note: File paths are resolved relative to the configuration file’s location.

**Future Source Types** Future releases will support additional source types:
- **Git repositories** (`type: "git"`) for loading server code directly from version control
- **FastMCP Cloud** (`type: "cloud"`) for hosted servers with automatic scaling and management

### Environment Configuration

The environment configuration determines **WHAT** environment setup your server requires. It controls the build-time setup of your Python environment, ensuring your server runs with the exact Python version and dependencies it requires. This section creates isolated, reproducible environments across different systems.FastMCP uses an extensible environment system with a base `Environment` class that can be implemented by different environment providers. Currently, FastMCP supports the `UVEnvironment` for Python environment management using `uv` ’s powerful dependency resolver.

## Environmentenvironment

object

Optional environment configuration. When specified, FastMCP uses the appropriate environment implementation to set up your server’s runtime.type

string

default:"uv"

The environment type identifier that determines which implementation to use. Currently supports `"uv"` for Python environments managed by uv. If omitted, defaults to `"uv"`.

ShowUVEnvironment

When `type` is `"uv"` (or omitted), the environment uses uv to manage Python dependencies:python

string

Python version constraint. Examples:
- Exact version: `"3.12"`
- Minimum version: `">=3.10"`
- Version range: `">=3.10,<3.13"`dependencies

list\[str\]

List of pip packages with optional version specifiers (PEP 508 format).

```
"dependencies": ["pandas>=2.0", "requests", "httpx"]
```requirements

string

Path to a requirements.txt file, resolved relative to the config file location.

```
"requirements": "requirements.txt"
```project

string

Path to a project directory containing pyproject.toml for uv project management.

```
"project": "."
```

**Example:**

```
"environment": {

  "type": "uv",

  "python": ">=3.10",

  "dependencies": ["pandas", "numpy"],

  "editable": ["."]

}
```

Note: When any UVEnvironment field is specified, FastMCP automatically creates an isolated environment using `uv` before running your server.

When environment configuration is provided, FastMCP:
1. Detects the environment type (defaults to `"uv"` if not specified)
2. Creates an isolated environment using the appropriate provider
3. Installs the specified dependencies
4. Runs your server in this clean environment
This build-time setup ensures your server always has the dependencies it needs, without polluting your system Python or conflicting with other projects.

**Future Environment Types** Similar to source types, future releases may support additional environment types for different runtime requirements, such as Docker containers or language-specific environments beyond Python.

### Deployment Configuration

The deployment configuration controls **HOW** your server runs. It defines the runtime behavior including network settings, environment variables, and execution context. These settings determine how your server operates when it executes, from transport protocols to logging levels.Environment variables are included in this section because they’re runtime configuration that affects how your server behaves when it executes, not how its environment is built. The deployment configuration is applied every time your server starts, controlling its operational characteristics.

## Deployment Fieldsdeployment

object

Optional runtime configuration for the server.transport

string

default:"stdio"

Protocol for client communication:
- `"stdio"`: Standard input/output for desktop clients
- `"http"`: Network-accessible HTTP server
- `"sse"`: Server-sent eventshost

string

default:"127.0.0.1"

Network interface to bind (HTTP transport only):
- `"127.0.0.1"`: Local connections only
- `"0.0.0.0"`: All network interfacesport

integer

default:"3000"

Port number for HTTP transport.path

string

default:"/mcp/"

URL path for the MCP endpoint when using HTTP transport.log\_level

string

default:"INFO"

Server logging verbosity. Options:
- `"DEBUG"`: Detailed debugging information
- `"INFO"`: General informational messages
- `"WARNING"`: Warning messages
- `"ERROR"`: Error messages only
- `"CRITICAL"`: Critical errors onlyenv

object

Environment variables to set when running the server. Supports `${VAR_NAME}` syntax for runtime interpolation.

```
"env": {

  "API_KEY": "secret-key",

  "DATABASE_URL": "postgres://${DB_USER}@${DB_HOST}/mydb"

}
```cwd

string

Working directory for the server process. Relative paths are resolved from the config file location.args

list\[str\]

Command-line arguments to pass to the server, passed after `--` to the server’s argument parser.

```
"args": ["--config", "server-config.json"]
```

#### Environment Variable Interpolation

The `env` field in deployment configuration supports runtime interpolation of environment variables using `${VAR_NAME}` syntax. This enables dynamic configuration based on your deployment environment:

```
{

  "deployment": {

    "env": {

      "API_URL": "https://api.${ENVIRONMENT}.example.com",

      "DATABASE_URL": "postgres://${DB_USER}:${DB_PASS}@${DB_HOST}/myapp",

      "CACHE_KEY": "myapp_${ENVIRONMENT}_${VERSION}"

    }

  }

}
```

When the server starts, FastMCP replaces `${ENVIRONMENT}`, `${DB_USER}`, etc. with values from your system’s environment variables. If a variable doesn’t exist, the placeholder is preserved as-is.**Example**: If your system has `ENVIRONMENT=production` and `DB_HOST=db.example.com`:

```
// Configuration

{

  "deployment": {

    "env": {

      "API_URL": "https://api.${ENVIRONMENT}.example.com",

      "DB_HOST": "${DB_HOST}"

    }

  }

}

// Result at runtime

{

  "API_URL": "https://api.production.example.com",

  "DB_HOST": "db.example.com"

}
```

This feature is particularly useful for:
- Deploying the same configuration across development, staging, and production
- Keeping sensitive values out of configuration files
- Building dynamic URLs and connection strings
- Creating environment-specific prefixes or suffixes

## Usage with CLI Commands

FastMCP automatically detects and uses a file specifically named `fastmcp.json` in the current directory, making server execution simple and consistent. Files with FastMCP configuration format but different names are not auto-detected and must be specified explicitly:

```
# Auto-detect fastmcp.json in current directory

cd my-project

fastmcp run  # No arguments needed!

# Or specify a configuration file explicitly

fastmcp run prod.fastmcp.json

# Skip environment setup when already in a uv environment

fastmcp run fastmcp.json --skip-env

# Skip source preparation when source is already prepared

fastmcp run fastmcp.json --skip-source

# Skip both environment and source preparation

fastmcp run fastmcp.json --skip-env --skip-source
```

### Pre-building Environments

You can use `fastmcp project prepare` to create a persistent uv project with all dependencies pre-installed:

```
# Create a persistent environment

fastmcp project prepare fastmcp.json --output-dir ./env

# Use the pre-built environment to run the server

fastmcp run fastmcp.json --project ./env
```

This pattern separates environment setup (slow) from server execution (fast), useful for deployment scenarios.

### Using an Existing Environment

By default, FastMCP creates an isolated environment with `uv` based on your configuration. When you already have a suitable Python environment, use the `--skip-env` flag to skip environment creation:

```
fastmcp run fastmcp.json --skip-env
```

**When you already have an environment:**
- You’re in an activated virtual environment with all dependencies installed
- You’re inside a Docker container with pre-installed dependencies
- You’re in a CI/CD pipeline that pre-builds the environment
- You’re using a system-wide installation with all required packages
- You’re in a uv-managed environment (prevents infinite recursion)
This flag tells FastMCP: “I already have everything installed, just run the server.”

### Using an Existing Source

When working with source types that require preparation (future support for git repositories or cloud sources), use the `--skip-source` flag when you already have the source code available:

```
fastmcp run fastmcp.json --skip-source
```

**When you already have the source:**
- You’ve previously cloned a git repository and don’t need to re-fetch
- You have a cached copy of a cloud-hosted server
- You’re in a CI/CD pipeline where source checkout is a separate step
- You’re iterating locally on already-downloaded code
This flag tells FastMCP: “I already have the source code, skip any download/clone steps.” Note: For filesystem sources (local Python files), this flag has no effect since they don’t require preparation.The configuration file works with all FastMCP commands:
- **`run`** - Start the server in production mode
- **`dev`** - Launch with the Inspector UI for development
- **`inspect`** - View server capabilities and configuration
- **`install`** - Install to Claude Desktop, Cursor, or other MCP clients
When no file argument is provided, FastMCP searches the current directory for `fastmcp.json`. This means you can simply navigate to your project directory and run `fastmcp run` to start your server with all its configured settings.

### CLI Override Behavior

Command-line arguments take precedence over configuration file values, allowing ad-hoc adjustments without modifying the file:

```
# Config specifies port 3000, CLI overrides to 8080

fastmcp run fastmcp.json --port 8080

# Config specifies stdio, CLI overrides to HTTP

fastmcp run fastmcp.json --transport http

# Add extra dependencies not in config

fastmcp run fastmcp.json --with requests --with httpx
```

This precedence order enables:
- Quick testing of different settings
- Environment-specific overrides in deployment scripts
- Debugging with increased log levels
- Temporary configuration changes

### Custom Naming Patterns

You can use different configuration files for different environments:
- `fastmcp.json` - Default configuration
- `dev.fastmcp.json` - Development settings
- `prod.fastmcp.json` - Production settings
- `test_fastmcp.json` - Test configuration
Any file with “fastmcp.json” in the name is recognized as a configuration file.

## Examples

A minimal configuration for a simple server:

```
{

  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",

  "source": {

    "path": "server.py",

    "entrypoint": "mcp"

  }

}
```

This configuration explicitly specifies the server entrypoint (`mcp`), making it clear which server instance or factory function to use. Uses all defaults: STDIO transport, no special dependencies, standard logging.

## Migrating from CLI Arguments

If you’re currently using command-line arguments or shell scripts, migrating to `fastmcp.json` simplifies your workflow. Here’s how common CLI patterns map to configuration:**CLI Command**:

```
uv run --with pandas --with requests \

  fastmcp run server.py \

  --transport http \

  --port 8000 \

  --log-level INFO
```

**Equivalent fastmcp.json**:

```
{

  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",

  "source": {

    "path": "server.py",

    "entrypoint": "mcp"

  },

  "environment": {

    "dependencies": ["pandas", "requests"]

  },

  "deployment": {

    "transport": "http",

    "port": 8000,

    "log_level": "INFO"

  }

}
```

Now simply run:

```
fastmcp run  # Automatically finds and uses fastmcp.json
```

The configuration file approach provides better documentation, easier sharing, and consistent execution across different environments while maintaining the flexibility to override settings when needed.