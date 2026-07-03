from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from nodes.parse_intent import make_parse_intent_node
from nodes.search_flights import make_search_flights_node
from nodes.check_policy import make_checks_policy_node
from nodes.build_response import build_response_node
from langgraph.graph import StateGraph, START, END
from state import AgentState

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
    parse_intent = make_parse_intent_node(model)
    search_flights = make_search_flights_node(tools_by_name)
    check_policy = make_checks_policy_node(tools_by_name)
    build_response = build_response_node(model)
    
    graph = StateGraph(AgentState)
    graph.add_node('parse_intent', parse_intent)
    graph.add_node('search_flights', search_flights)
    graph.add_node('check_policy', check_policy)
    graph.add_node('build_response', build_response)
    
    graph.add_edge(START, 'parse_intent')
    graph.add_edge('parse_intent', 'search_flights')
    graph.add_edge('search_flights', 'check_policy')
    graph.add_edge('check_policy', 'build_response')
    graph.add_edge('build_response', END)
    
    travel_graph = graph.compile()
    
    result = await travel_graph.ainvoke({'messages': HumanMessage(content='I am EMP001 and I want to fly from PHX to JFK on July 19th')})
    print(f'Result: {result}')
asyncio.run(main())

