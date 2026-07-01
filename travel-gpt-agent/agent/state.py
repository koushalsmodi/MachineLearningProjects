"""State management for the travel GPT agent."""

from langgraph.graph import MessagesState

class AgentState(MessagesState):
    
    # Traveler's request
    employee_id: int
    origin: str
    destination: str
    departure_date: str
    cabin_preference: str
    
    # From Flight Search server
    flight_results: list
    
    # From Traveler lookup server
    traveler_dict: dict
    traveler_tier:  str
    
    # From Policy server
    cabin_class_response_dict: dict
    approved_airline_response_dict: dict
    advance_booking_response_dict: dict
    upgrade_eligibility_response_dict: dict
    budget_response_dict: dict
    
    compliant_flights: list
    non_compliant_flights: list
    
    # From Budget server
    remaining_budget: float
    budget_status: bool
    
    # Response
    response: str 
    booking_status: str