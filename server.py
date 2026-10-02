from mcp.server.fastmcp import FastMCP

# Create the server and give it a name
mcp = FastMCP("my-first-server")


# TOOL: an action the AI can run
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def secret_number() -> int:
    """Return the secret number"""
    return 7391

    
# RESOURCE: read-only data
@mcp.resource("notes://today")
def today_notes() -> str:
    """Today's notes"""
    return "Meeting at 3 PM. Finish MCP learning."


# PROMPT: a reusable template
@mcp.prompt()
def review_code(code: str) -> str:
    """Ask the AI to review code"""
    return f"Review this code for bugs and suggest improvements:\n\n{code}"


# if __name__ == "__main__":
#     mcp.run(transport="stdio")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")