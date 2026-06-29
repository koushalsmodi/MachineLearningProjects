from fastmcp import FastMCP
from budget_tracker import get_remaining_budget, deduct_budget

mcp = FastMCP(
    "budget-server",
    instructions = "Use these tools to get check Traveler's budget for booking"
)

# defining a tool
@mcp.tool()
def remaining_budget(team_entered):
    """ 
    Retrieve the remaining travel budget for a team. Use this before
    approving any booking to verify sufficient funds remain.
    """
    return get_remaining_budget(team_entered)

@mcp.tool()
def budget_deduct(team_entered, amount):
    """ 
    Deduct a confirmed booking amount from a team's remaining travel budget. Use this only
    after a booking has been approved and all policy checks have passed.
    """
    return deduct_budget(team_entered, amount)


if __name__ == "__main__":
    mcp.run()