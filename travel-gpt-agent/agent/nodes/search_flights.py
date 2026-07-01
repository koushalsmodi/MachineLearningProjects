import sys
sys.path.append('/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent')
from agent.state import AgentState
import json

def make_search_flights_node(tools_by_name):
    async def search_flights(state: AgentState) -> AgentState:
        origin = state['origin']
        destination = state['destination']
        departure_date = state['departure_date']
        cabin_preference = state['cabin_preference']
        
        result = await tools_by_name['flight_search'].ainvoke({
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "cabin_class": cabin_preference
        })
        
        result = json.loads(result[0]['text'])
        return {"flight_results": result}
    return search_flights 
