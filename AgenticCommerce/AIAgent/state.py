from pydantic import BaseModel
from typing import List


class AgentState(BaseModel):
    
    """
    Unified summary of the agent state workflow
    
    User Input -> Planning Agent -> Research Agent -> Optimization Agent -> Risk Agent -> Payment Agent -> Confirmation Agent
    
    """
    # User Input
    user_request: str 
    user_id: str 

    # Agent 1: PlanningAgent
    destination: str | None = None
    travel_dates: List[str] = [] 
    budget: float | None = None
    preferences: List[str] = [] 
    
    # Agent 2: ResearchAgent
    flight_options: List[dict] = []
    hotel_options: List[dict] = []
    restaurant_options: List[dict] = []

    # Agent 3: OptimizationAgent
    selected_flight: dict | None = None
    selected_hotel: dict | None = None
    selected_restaurant: dict | None = None
    points_earned: int = 0
    applied_offers: List[dict] = []
    original_cost: float = 0.0
    final_cost: float = 0.0
    
    # Agent 4: RiskAgent
    risk_score: float = 0.0
    risk_flags: List[str] = [] 
    requires_approval: bool = False
    risk_analysis: List[dict] = [] 
    
    # Agent 5: PaymentAgent
    payment_status: str | None = None
    transaction_id: str | None = None
    payment_timestamp: str | None = None
    booking_confirmations: List[dict] = [] 
    
    # Agent 6: ConfirmationAgent
    confirmation_message: str | None = None
    audit_trail: List[dict] = []
    
    # ErrorHandling(BaseModel):
    errors: List[str] = [] 
    retry_count: int = 0
    
if __name__ == '__main__':
    # Test 1: Create initial state
    state = AgentState(
        user_request= "Book me a trip to Miami",
        user_id = "ksm_124"
    )
    
    print("Initial State Created:", state.user_request, state.user_id)
    
    state.destination = 'Miami'
    state.budget = 2000.0
    state.travel_dates = ['2026-02-24', '2026-03-01']
    
    print("Planning Agent:", state.destination, state.budget, state.travel_dates)
    
    state.flight_options = [
        {"flight_id": "EA1", "price": 250.0, "airline": "Emirates"},
        {"flight_id": "LA19", "price": 420.0, "airline": "Lufthansa"}
    ]
    
    print("Research Agent:", state.flight_options)
    
    print("Default risk score:", state.risk_score)
    print("Default risk flags:", state.risk_flags)
    print("Default requires approval:", state.requires_approval)
    print("Default risk analysis:", state.risk_analysis)
    print("Default errors:", state.errors)
    
