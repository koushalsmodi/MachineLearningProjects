from state import AgentState
from tools.llm_utils import call_claude
import json

def planning_node(state: AgentState) -> AgentState:
    """ 
    Input:
        user_request: str 
        user_id: str 
    
    Output:
        Destination: Miami, FL
        Travel dates: ['2026-03-15', '2026-03-17']
        Budget: 2000.0
        Preferences: ['weekend trip', 'beachfront hotel']
    """
    
    user_request = state.user_request

    system_prompt = """
    You are a travel planning assistant that extracts structured information.

    Extract from the user request and return only valid JSON in this exact format:
    {
    "destination": "City, State" (string),
    "travel_dates": ["YYYY-MM-DD", "YYYY-MM-DD"] (list of date strings, empty if not specified),
    "budget": 2000.0 (float number only, no currency),
    "preferences": ["preference1", "preference2"] (list of strings)
    }
    """
    
    prompt = f"Extract travel info from: {user_request}"
    response = call_claude(prompt = prompt, system_prompt = system_prompt)
    # print("Claude's raw response:")
    # print(response)
    
    cleaned_response = response.strip()
    if cleaned_response.startswith("```"):
        # Remove opening ```json or ```
        cleaned_response = cleaned_response.split("\n", 1)[1]
        # Remove closing ```
        cleaned_response = cleaned_response.rsplit("```", 1)[0]
        cleaned_response = cleaned_response.strip()

    # this converts a JSON string into a real Python object (dict / list).
    # json.loads() is for string as input
    # json.load() is for file as input
    try:
        data = json.loads(cleaned_response)
    except Exception as e:
        return f"Error occurred: {e}"
    
    state.destination = data.get("destination")
    state.travel_dates = data.get("travel_dates")
    state.budget = data.get("budget")
    state.preferences = data.get("preferences")
    
    return state

if __name__ == '__main__':
    # Test: Create initial state
    test_state = AgentState(
        user_request= "Book me a trip to Miami for the weekend in less than $5000",
        user_id = "ksm_124"
    )
    
    updated_state = planning_node(test_state)
    
    print(f"Updated State: {updated_state}")
