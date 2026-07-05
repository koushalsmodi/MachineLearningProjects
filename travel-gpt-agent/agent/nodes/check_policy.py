import sys
sys.path.append('/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent')
from agent.state import AgentState
import json

def make_checks_policy_node(tools_by_name):
    async def check_policy(state: AgentState) -> AgentState:
        employee_id = state['employee_id']
        
        traveler_tier = await tools_by_name['get_traveler_tier_info'].ainvoke({
        "employee_id": employee_id
        })
        
        traveler_tier = traveler_tier[0]['text']
        traveler_team = await tools_by_name['get_traveler_team_info'].ainvoke({
                                "employee_id": employee_id
                            })
        print('raw team result', traveler_team)
        traveler_team = traveler_team[0]['text']
        print('team name:', traveler_team)
        flight_results = state['flight_results']
        
        # From Policy server
        compliant_flights = []
        non_compliant_flights = []
        
        for flight in flight_results:
            airline_check_failed = False
            failed_airline_reason = None

            for leg in flight['legs']:
                leg_airline_result = await tools_by_name['approved_airline'].ainvoke({
                    "tier": traveler_tier,
                    "airline": leg['airline']
                })
                leg_airline_result = json.loads(leg_airline_result[0]['text'])

                if leg_airline_result['status'] == 'fail':
                    airline_check_failed = True
                    failed_airline_reason = f"{leg['airline']}: {leg_airline_result['reason']}"
                    break

            if airline_check_failed:
                non_compliant_flights.append({
                    'flight': flight,
                    'failed_check': 'approved_airline',
                    'reason': failed_airline_reason
                })
                continue

            departure_date = state['departure_date']
            advance_booking_result = await tools_by_name['advance_booking'].ainvoke({
                "tier": traveler_tier,
                "departure_date": departure_date
            })
            advance_booking_result = json.loads(advance_booking_result[0]['text'])

            if advance_booking_result['status'] == 'fail':
                non_compliant_flights.append({
                    'flight': flight,
                    'failed_check': 'advance_booking',
                    'reason': advance_booking_result['reason']
                })
                continue

            cabin_requested = state.get('cabin_preference')
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

            estimated_cost_requested = flight.get('price', 0)
            estimated_cost_result = await tools_by_name['budget_check'].ainvoke({
                "tier": traveler_tier,
                "estimated_cost": estimated_cost_requested
            })
            estimated_cost_result = json.loads(estimated_cost_result[0]['text'])

            if estimated_cost_result['status'] == 'fail':
                non_compliant_flights.append({
                    'flight': flight,
                    'failed_check': 'budget_check',
                    'reason': estimated_cost_result['reason']
                })
                continue

            remaining_budget_result = await tools_by_name['remaining_budget'].ainvoke({
                "team_entered": traveler_team
            })
            remaining_budget_value = float(remaining_budget_result[0]['text'])

            if remaining_budget_value < estimated_cost_requested:
                non_compliant_flights.append({
                    'flight': flight,
                    'failed_check': 'remaining_budget',
                    'reason': f"Flight price ${flight['price']} exceeds team remaining budget ${remaining_budget_value}"
                })
                continue

            compliant_flights.append(flight)
                
        #print(result)
        # check_advance_booking(tier, departure_date)
        
        return {
        'traveler_tier': traveler_tier,
        'traveler_team': traveler_team,
        'compliant_flights': compliant_flights,
        'non_compliant_flights': non_compliant_flights
        #'advance_booking_result': advance_booking_result,
        #'cabin_class_result': cabin_class_result,
        #'estimated_cost_result': estimated_cost_result
        }
    
    return check_policy 