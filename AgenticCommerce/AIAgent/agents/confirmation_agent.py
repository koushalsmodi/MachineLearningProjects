from state import AgentState

def confirmation_node(state: AgentState) -> AgentState:
    """Generate final confirmation message and audit trail
    
    Input:
    state.selected_flight = {"airline": "Emirates", "price": 250.0, ...}
    state.selected_hotel = {"name": "Taj South Beach", ...}
    state.selected_restaurant = {"name": "Joe's Stone Crab", ...}
    state.final_cost = 738.0
    state.points_earned = 1990
    state.transaction_id = "TXN-20260215-B4I0QZ"
    state.booking_confirmations = [...]
    state.applied_offers = [...]
    
    Output:
    state.confirmation_message = "Beautiful formatted receipt"
    state.audit_trail = ["Planning completed", "Research found 10 flights", ...]
    """
    
    # 1. Build confirmation message (formatted receipt)
    confirmation_message = generate_confirmation_message(state)
    
    # 2. Build audit trail (log of what happened)
    audit_trail = generate_audit_trail(state)
    
    # 3. Update state
    state.confirmation_message = confirmation_message
    state.audit_trail = audit_trail
    
    return state

def generate_confirmation_message(state: AgentState) -> str:
    """Generate beautifully formatted confirmation receipt."""
    
    # Extract confirmation codes
    flight_conf = ""
    hotel_conf = ""
    restaurant_conf = ""
    
    for booking in state.booking_confirmations:
        if booking["type"] == "flight":
            flight_conf = booking["confirmation"]
        elif booking["type"] == "hotel":
            hotel_conf = booking["confirmation"]
        elif booking["type"] == "restaurant":
            restaurant_conf = booking["confirmation"]
    
    # Build formatted message
    message = f"""
    🎉 BOOKING CONFIRMED 🎉

    Transaction ID: {state.transaction_id}
    Payment Status: {state.payment_status}

    {'='*60}
    ✈️ FLIGHT
    {'='*60}
    Airline: {state.selected_flight['airline']}
    Price: ${state.selected_flight['price']:.2f}
    Route: {state.selected_flight['origin']} → {state.selected_flight['destination']}
    Confirmation: {flight_conf}

    {'='*60}
    🏨 HOTEL
    {'='*60}
    Name: {state.selected_hotel['name']}
    Price: ${state.selected_hotel['price_per_night']:.2f}/night
    Location: {state.selected_hotel['location_type']}
    Confirmation: {hotel_conf}

    {'='*60}
    🍽️ RESTAURANT
    {'='*60}
    Name: {state.selected_restaurant['name']}
    Cuisine: {state.selected_restaurant['cuisine_type']}
    Price: ${state.selected_restaurant['avg_cost_per_person']:.2f}/person
    Confirmation: {restaurant_conf}

    {'='*60}
    💰 COST SUMMARY
    {'='*60}
    Original Cost: ${state.original_cost:.2f}
    Final Cost: ${state.final_cost:.2f}
    You Saved: ${state.original_cost - state.final_cost:.2f}

    {'='*60}
    🎁 REWARDS
    {'='*60}
    Points Earned: {state.points_earned:,} points

    Thank you for booking with us!
    """
    
    return message.strip()

def generate_audit_trail(state: AgentState) -> list:
    """Generate audit trail documenting the booking process."""
    
    trail = []
    
    # Planning
    trail.append(f"Planning: Extracted destination={state.destination}, budget=${state.budget}")
    
    # Research
    trail.append(f"Research: Found {len(state.flight_options)} flights, {len(state.hotel_options)} hotels, {len(state.restaurant_options)} restaurants")
    
    # Optimization
    trail.append(f"Optimization: Selected {state.selected_flight['airline']} flight, {state.selected_hotel['name']}, {state.selected_restaurant['name']}")
    trail.append(f"Optimization: Applied {len(state.applied_offers)} offers, earned {state.points_earned} points")
    
    # Risk
    trail.append(f"Risk: Risk score {state.risk_score:.2f}, {'REQUIRES APPROVAL' if state.requires_approval else 'approved automatically'}")
    
    # Payment
    trail.append(f"Payment: Transaction {state.transaction_id} {state.payment_status}")
    
    return trail

if __name__ == "__main__":
    from agents.planning_agent import planning_node
    from agents.research_agent import research_node
    from agents.optimization_agent import optimization_node
    from agents.risk_agent import risk_node
    from agents.payment_agent import payment_node
    
    # Full pipeline test
    initial_state = AgentState(
        user_request="Book me a trip to Miami under $2000",
        user_id="ksm_124"
    )
    
    state = planning_node(initial_state)
    state = research_node(state)
    state = optimization_node(state)
    state = risk_node(state)
    state = payment_node(state)
    state = confirmation_node(state)
    
    # Print beautiful output
    print(state.confirmation_message)
    
    print("\n" + "="*60)
    print("AUDIT TRAIL")
    print("="*60)
    for entry in state.audit_trail:
        print(f"  • {entry}")