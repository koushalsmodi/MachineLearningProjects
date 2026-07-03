import sys
sys.path.append('/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent')
from agent.state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage


base_dir = '/Users/koushalsmodi/Desktop/MachineLearning/MachineLearningProjects/travel-gpt-agent/agent/prompts/'


def build_response_node(model):
    def build_response_from_state(state: AgentState) -> AgentState:
        with open(base_dir + 'build_response.txt', 'r') as f:
            system_prompt = f.read()
            # print(system_prompt)
        
        state_prompt = f"""
            traveler_tier: {state['traveler_tier']}\n
            employee_id: {state['employee_id']}\n
            origin: {state['origin']}\n
            destination: {state['destination']}\n
            departure_date: {state['departure_date']}\n
            cabin_preference: {state['cabin_preference']}\n
            compliant_flights: {state['compliant_flights']}\n
            non_compliant_flights: {state['non_compliant_flights']}\n
        """
        
        if state['compliant_flights']:
            booking_status = "compliant"
        
        elif state['non_compliant_flights']:
            booking_status = "non-compliant"
            
        else:
            booking_status = "no flights found"
        
        sys_msg = SystemMessage(content=system_prompt)
        human_prompt = "Use the above to build the final response."
        human_msg = HumanMessage(content = f'{human_prompt}\n\n{state_prompt}')
        messages = [sys_msg, human_msg]

        response = model.invoke(messages)
        response = response.content
    
        return {
                'response': response,
                'booking_status': booking_status
        }
    return build_response_from_state
