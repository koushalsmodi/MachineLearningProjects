from fastmcp import FastMCP
from serpapi_client import search_flights

mcp = FastMCP(
    "search-flights-server",
    instructions = "Use the search_flights tool to search for best flights possible based on origin, destination, departure_date, cabin_class"
)

# defining a tool
@mcp.tool()
def flight_search(origin, destination, departure_date, cabin_class):
    """ 
    Use the search_flights tool to search for best flights possible based on origin, 
    destination, departure_date, cabin_class
    
    """
    return search_flights(origin, destination, departure_date, cabin_class)


if __name__ == "__main__":
    mcp.run()