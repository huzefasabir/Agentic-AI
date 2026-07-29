from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Maths")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers. Always return a number, not a function."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two integers. Inputs must be plain integers."""
    return a * b


if __name__=="__main__":
    mcp.run(transport="stdio")
    #the transport stdio tells the server to:
    #use the standard i/o (stdin /stdout)tp receive and respond to tool function calls