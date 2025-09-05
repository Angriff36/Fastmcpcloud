---
title: "ChatGPT 🤝 FastMCP"
source: "https://gofastmcp.com/integrations/chatgpt"
author:
  - "[[Eunomia Auth]]"
published:
created: 2025-09-04
description: "Connect FastMCP servers to ChatGPT Deep Research"
tags:
  - "clippings"
---
ChatGPT supports MCP servers through remote HTTP connections, allowing you to extend ChatGPT’s capabilities with custom tools and knowledge from your FastMCP servers.

MCP integration with ChatGPT is currently limited to **Deep Research** functionality and is not available for general chat. This feature is available for ChatGPT Pro, Team, Enterprise, and Edu users.

OpenAI’s official MCP documentation and examples are built with **FastMCP v2**! Check out their [simple Deep Research-style MCP server example](https://github.com/openai/sample-deep-research-mcp) for a quick reference similar to the one in this document, or their [more complete Deep Research example](https://github.com/openai/openai-cookbook/tree/main/examples/deep_research_api/how_to_build_a_deep_research_mcp_server) from the OpenAI Cookbook, which includes vector search and more.

## Deep Research

ChatGPT’s Deep Research feature requires MCP servers to be internet-accessible HTTP endpoints with **exactly two specific tools**:
- **`search`**: For searching through your resources and returning matching IDs
- **`fetch`**: For retrieving the full content of specific resources by ID

If your server doesn’t implement both `search` and `fetch` tools with the correct signatures, ChatGPT will show the error: “This MCP server doesn’t implement our specification”. Both tools are required.

### Tool Descriptions Matter

Since ChatGPT needs to understand how to use your tools effectively, **write detailed tool descriptions**. The description teaches ChatGPT how to form queries, what parameters to use, and what to expect from your data. Poor descriptions lead to poor search results.

### Create a Server

A Deep Research-compatible server must implement these two required tools:
- **`search(query: str)`** - Takes a query of any kind and returns matching record IDs
- **`fetch(id: str)`** - Takes an ID and returns the record
**Critical**: Write detailed docstrings for both tools. These descriptions teach ChatGPT how to use your tools effectively. Poor descriptions lead to poor search results.The `search` tool should take a query (of any kind!) and return IDs. The `fetch` tool should take an ID and return the record.Here’s a reference server implementation you can adapt (see also [OpenAI’s sample server](https://github.com/openai/sample-deep-research-mcp) for comparison):

server.py

```
import json

from pathlib import Path

from dataclasses import dataclass

from fastmcp import FastMCP

@dataclass

class Record:

    id: str

    title: str

    text: str

    metadata: dict

def create_server(

    records_path: Path | str,

    name: str | None = None,

    instructions: str | None = None,

) -> FastMCP:

    """Create a FastMCP server that can search and fetch records from a JSON file."""

    records = json.loads(Path(records_path).read_text())

    RECORDS = [Record(**r) for r in records]

    LOOKUP = {r.id: r for r in RECORDS}

    mcp = FastMCP(name=name or "Deep Research MCP", instructions=instructions)

    @mcp.tool()

    async def search(query: str):

        """

        Simple unranked keyword search across title, text, and metadata.

        Searches for any of the query terms in the record content.

        Returns a list of matching record IDs for ChatGPT to fetch.

        """

        toks = query.lower().split()

        ids = []

        for r in RECORDS:

            record_txt = " ".join(

                [r.title, r.text, " ".join(r.metadata.values())]

            ).lower()

            if any(t in record_txt for t in toks):

                ids.append(r.id)

        return {"ids": ids}

    @mcp.tool()

    async def fetch(id: str):

        """

        Fetch a record by ID.

        Returns the complete record data for ChatGPT to analyze and cite.

        """

        if id not in LOOKUP:

            raise ValueError(f"Unknown record ID: {id}")

        return LOOKUP[id]

    return mcp

if __name__ == "__main__":

    mcp = create_server("path/to/records.json")

    mcp.run(transport="http", port=8000)
```

### Deploy the Server

Your server must be deployed to a public URL in order for ChatGPT to access it.For development, you can use tools like `ngrok` to temporarily expose a locally-running server to the internet. We’ll do that for this example (you may need to install `ngrok` and create a free account), but you can use any other method to deploy your server.Assuming you saved the above code as `server.py`, you can run the following two commands in two separate terminals to deploy your server and expose it to the internet:

```
python server.py
```

This exposes your unauthenticated server to the internet. Only run this command in a safe environment if you understand the risks.

### Connect to ChatGPT

Replace `https://your-server-url.com` with the actual URL of your server (such as your ngrok URL).
1. Open ChatGPT and go to **Settings** → **Connectors**
2. Click **Add custom connector**
3. Enter your server details:
	- **Name**: Library Catalog
	- **URL**: Your server URL, including the path.
		- **Note**: Ensure your URL includes the correct path for the transport you’re using. The defaults are /sse/ for SSE (e.g., [https://abc123.ngrok.io/sse/](https://abc123.ngrok.io/sse/)) and /mcp/ for HTTP (e.g., [https://abc123.ngrok.io/mcp/](https://abc123.ngrok.io/mcp/)).
	- **Description**: A library catalog for searching and retrieving books

#### Test the Connection

1. Start a new chat in ChatGPT
2. Click **Tools** → **Run deep research**
3. Select your **Library Catalog** connector as a source
4. Ask questions like:
	- “Search for Python programming books”
	- “Find books about AI and machine learning”
	- “Show me books by the Python Software Foundation”
ChatGPT will use your server’s search and fetch tools to find relevant information and cite the sources in its response.

### Troubleshooting

#### ”This MCP server doesn’t implement our specification”

If you get this error, it most likely means that your server doesn’t implement the required tools (`search` and `fetch`). To correct it, ensure that your server meets the service requirements.