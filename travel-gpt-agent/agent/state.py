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
    traveler_tier:  str
    traveler_team: str

    compliant_flights: list
    non_compliant_flights: list
    
    
    # Response
    response: str 
    booking_status: str