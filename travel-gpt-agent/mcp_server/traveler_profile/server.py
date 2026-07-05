from fastmcp import FastMCP
from profile_loader import get_traveler, get_traveler_tier, get_traveler_team_name
import json

mcp = FastMCP(
    "traveler-profile-server",
    instructions = "Use these tools to get Traveler's information and tier"
)

# defining a tool
@mcp.tool()
def get_traveler_info(employee_id):
    """ Retrieve full profile of a Corporate Traveler including their
    tier, team, home airport, loyalty programs and budget pool.
    Use this when you need complete traveler information.
    """
    return json.dumps(get_traveler(employee_id=employee_id))
    
@mcp.tool()
def get_traveler_team_info(employee_id):
    """ Retrieve the team name of a Corporate Traveler
    Use this when you need traveler's team name information.
    """
    return get_traveler_team_name(employee_id)

@mcp.tool()
def get_traveler_tier_info(employee_id):
    """ Retrieve tier (entry/ manager/ senior) of a Corporate Traveler
    Use this when you need traveler's tier information.
    """
    return get_traveler_tier(employee_id=employee_id)

if __name__ == "__main__":
    mcp.run()