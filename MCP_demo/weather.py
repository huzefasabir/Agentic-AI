from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(location:str)->str:
    """ Get the weather of the location """
    return f"The weather of {location} is sunny"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
    # the transport stdio tells the server to:
    # use the standard i/o (stdin/stdout) to receive and respond to tool function calls