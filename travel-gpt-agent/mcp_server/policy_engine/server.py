from fastmcp import FastMCP
from checks import check_cabin_class, check_approved_airline, check_advance_booking, check_upgrade_eligibility, check_budget

mcp = FastMCP(
    "policy-engine-server",
    instructions = "Use these tools to get check Traveler's information for booking"
)

# defining a tool
@mcp.tool()
def cabin_class(tier, cabin_requested):
    """ 
    Check if the requested cabin class is permitted for the traveler's policy tier
    """
    return check_cabin_class(tier, cabin_requested)
    

@mcp.tool()
def approved_airline(tier, airline):
    """ 
    Check if the requested airline is permitted for the traveler's policy tier
    """
    return check_approved_airline(tier, airline)

@mcp.tool()
def advance_booking(tier, departure_date):
    """ 
    Check if the requested departure date is permitted for the traveler's policy tier
    """
    return check_advance_booking(tier, departure_date)

@mcp.tool()
def upgrade_eligibility(tier, upgrade_cost):
    """ 
    Check if the requested upgrade is permitted for the traveler's policy tier
    """
    return check_upgrade_eligibility(tier, upgrade_cost)

@mcp.tool()
def budget_check(tier, estimated_cost):
    """ 
    Check if the requested estimated cost is permitted for the traveler's policy tier
    """
    return check_budget(tier, estimated_cost)


if __name__ == "__main__":
    mcp.run()