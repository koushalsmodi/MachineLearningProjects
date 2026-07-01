from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

# initialize LLM
model = ChatAnthropic(
    model="claude-sonnet-4-6",
    anthropic_api_key = api_key
)

# initialize MultiServerMCPClient
server_config = {
    "traveler-profile-server": {
        "command": "python",
        "args": ["/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/mcp_server/traveler_profile/server.py"],
        "transport": "stdio"
    },
    "policy-engine-server":{
        "command": "python",
        "args": ["/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/mcp_server/policy_engine/server.py"],
        "transport": "stdio"
    },
    
    "budget-server":{
        "command": "python",
        "args": ["/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/mcp_server/budget/server.py"],
        "transport": "stdio"
    },
    
    "search-flights-server":{
        "command": "python",
        "args": ["/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/mcp_server/flight_search/server.py"],
        "transport": "stdio"
    },
}

async def main():
    client = MultiServerMCPClient(server_config)
    tools = await client.get_tools()
    # print(tools, '\n')
    tools_by_name = {tool.name: tool for tool in tools}
    
asyncio.run(main())

