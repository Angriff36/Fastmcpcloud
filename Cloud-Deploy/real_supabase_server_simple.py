#!/usr/bin/env python3
"""
Simplified version of our server with just one prompt to test
"""

from fastmcp import FastMCP

mcp = FastMCP("Prep Chef Database Server")

@mcp.tool
def test_connection() -> str:
    """Test basic functionality."""
    return "Server is working!"

@mcp.prompt
def simple_kitchen_prompt(task: str = "general guidance") -> str:
    """Generate kitchen guidance prompts."""
    return f"Please provide guidance for: {task}"

if __name__ == "__main__":
    print("🍳 Starting simplified Prep Chef server...")
    mcp.run()
