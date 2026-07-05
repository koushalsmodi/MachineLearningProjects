import sys
sys.path.append('/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent')
from agent.state import AgentState
import json

def make_lookup_origin_node(tools_by_name):
    async def lookup_origin(state: AgentState) -> AgentState:
        employee_id = state.get('employee_id')
        if not employee_id:
            return {}
        
        result = await tools_by_name['get_traveler_info'].ainvoke({
            'employee_id': employee_id
        })
        traveler_info_result = result[0]['text']
        
        try:
            traveler_info = json.loads(traveler_info_result)
        
        except json.JSONDecodeError:
            return {}
        
        return {'origin': traveler_info.get('home_airport')}
    
    return lookup_origin