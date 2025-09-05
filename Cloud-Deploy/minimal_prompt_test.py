#!/usr/bin/env python3
"""
Minimal test to check if prompts work at all
"""

from fastmcp import FastMCP

# Create a minimal server with one prompt
mcp = FastMCP("Test Server")

@mcp.prompt
def test_prompt(message: str = "Hello") -> str:
    """A simple test prompt."""
    return f"Test prompt says: {message}"

if __name__ == "__main__":
    print("🚀 Starting minimal server with test prompt...")
    mcp.run()
