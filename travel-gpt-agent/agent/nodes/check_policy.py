import sys
sys.path.append('/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent')
from agent.state import AgentState
from search_flights import make_search_flights_node
import json

def make_checks_policy_node(tools_by_name):
    async def check_policy(state: AgentState) -> AgentState:
        employee_id = state['employee_id']
        
        traveler_tier = await tools_by_name['get_traveler_tier_info'].ainvoke({
        "employee_id": employee_id
        })
        
        traveler_tier = traveler_tier[0]['text']
        
        flight_results = state['flight_results']
        
        # From Policy server
        compliant_flights = []
        non_compliant_flights = []
        
        for flight in flight_results:
            airline = flight['legs'][0]['airline']
            airline_result = await tools_by_name['approved_airline'].ainvoke({
                "tier": traveler_tier,
                "airline": airline
            })
            airline_result = json.loads(airline_result[0]['text'])
            
            departure_date = state['departure_date']
            advance_booking_result = await tools_by_name['advance_booking'].ainvoke({
            "tier": traveler_tier,
            "departure_date": departure_date
            })
            advance_booking_result = json.loads(advance_booking_result[0]['text'])
            
            if airline_result['status'] == 'fail':
                non_compliant_flights.append({
                    'flight': flight,
                    'failed_check': 'approved_airline',
                    'reason': airline_result['reason']
                })
                continue
            
            else:
                if advance_booking_result['status'] == 'fail':
                    non_compliant_flights.append({
                    'flight': flight,
                    'failed_check': 'advance_booking',
                    'reason': advance_booking_result['reason']
                    })
                    continue
                else:
                    cabin_requested = state['cabin_preference']
                    cabin_class_result = await tools_by_name['cabin_class'].ainvoke({
                    "tier": traveler_tier,
                    "cabin_requested": cabin_requested
                    })
                    cabin_class_result = json.loads(cabin_class_result[0]['text'])
                    if cabin_class_result['status'] == 'fail':
                        non_compliant_flights.append({
                        'flight': flight,
                        'failed_check': 'cabin_class',
                        'reason': cabin_class_result['reason']
                        })
                        continue
                    
                    else:
                        estimated_cost_requested = flight['price']
                        estimated_cost_result = await tools_by_name['budget_check'].ainvoke({
                        "tier": traveler_tier,
                        "estimated_cost_requested": estimated_cost_requested
                        })
                        estimated_cost_result = json.loads(estimated_cost_result[0]['text'])
                        if estimated_cost_result['status'] == 'fail':
                            non_compliant_flights.append({
                            'flight': flight,
                            'failed_check': 'budget_check',
                            'reason': estimated_cost_result['reason']
                            })
                            continue
                        else:
                            compliant_flights.append(flight)
                
        #print(result)
        # check_advance_booking(tier, departure_date)
        
        return {
        'traveler_tier': traveler_tier,
        'compliant_flights': compliant_flights,
        'non_compliant_flights': non_compliant_flights,
        'advance_booking_result': advance_booking_result,
        'cabin_class_result': cabin_class_result,
        'estimated_cost_result': estimated_cost_result
        }
    
    return check_policy 

if __name__ == "__main__":
    import asyncio
    from langchain_mcp_adapters.client import MultiServerMCPClient

    server_config = {
        "traveler-profile-server": {
            "command": "python",
            "args": ["/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/mcp_server/traveler_profile/server.py"],
            "transport": "stdio"
        },
        "policy-engine-server": {
            "command": "python",
            "args": ["/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/mcp_server/policy_engine/server.py"],
            "transport": "stdio"
        },
        "budget-server": {
            "command": "python",
            "args": ["/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/mcp_server/budget/server.py"],
            "transport": "stdio"
        },
        "search-flights-server": {
            "command": "python",
            "args": ["/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/mcp_server/flight_search/server.py"],
            "transport": "stdio"
        },
    }

    async def test():
        client = MultiServerMCPClient(server_config)
        tools = await client.get_tools()
        tools_by_name = {tool.name: tool for tool in tools}
        
        # Traveler's request from State
        """ 
        employee_id: int
        origin: str
        destination: str
        departure_date: str
        cabin_preference: str
        """
        
        fake_state = {
            "employee_id": "EMP001",
            "origin" : 'SFO',
            "destination":'JFK',
            "departure_date":'2026-07-16',
            "cabin_preference": 'economy'
        }
    
        # From Flight Search server
        check_search_flights_node = make_search_flights_node(tools_by_name)
        search_result = await check_search_flights_node(fake_state)
        fake_state['flight_results'] = search_result['flight_results']
        print("search_result:", search_result)
        
        
        check_policy_node = make_checks_policy_node(tools_by_name)
        result = await check_policy_node(fake_state)
        print("Final result:", result)

    asyncio.run(test())