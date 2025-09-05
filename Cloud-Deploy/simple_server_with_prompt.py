#!/usr/bin/env python3
"""
Simple server with one prompt to test
"""

from fastmcp import FastMCP

mcp = FastMCP("Simple Test Server")

@mcp.tool
def test_tool() -> str:
    """A simple test tool."""
    return "Hello from test tool!"

@mcp.prompt
def test_prompt(message: str = "Hello") -> str:
    """A simple test prompt."""
    return f"Test prompt says: {message}"

if __name__ == "__main__":
    print("🚀 Starting simple server with prompt...")
    mcp.run()
