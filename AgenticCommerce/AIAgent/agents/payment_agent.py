from state import AgentState
from agents.planning_agent import planning_node
from agents.research_agent import research_node
from agents.optimization_agent import optimization_node
from agents.risk_agent import risk_node
from datetime import datetime
import random
import string

def payment_node(state: AgentState) -> AgentState:
    """Process payment and generate booking confirmations."""
    
    # Step 1: Check approval requirement
    approval_requirement = state.requires_approval
    if approval_requirement:
        state.payment_status = "pending_approval"
        return state
        
    # Step 2: Generate transaction ID
    transaction_id = generate_transaction_id()
    
    # Step 3: Set payment status
    # Step 4: Set timestamp
    # Step 5: Generate booking confirmations
    
    selected_flight = state.selected_flight
    selected_hotel = state.selected_hotel
    selected_restaurant = state.selected_restaurant
    
    flight_cnf = generate_flight_confirmation(selected_flight)
    hotel_cnf = generate_hotel_confirmation(selected_hotel)
    restaurant_cnf = generate_restaurant_confirmation(selected_restaurant)
    
    booking_list = generate_booking_confirmations(flight_cnf, hotel_cnf, restaurant_cnf)
    
    # Step 6: Update state
    state.payment_status = "confirmed"
    state.transaction_id =  transaction_id
    state.payment_timestamp = datetime.now().isoformat()
    state.booking_confirmations = booking_list
    
    # Step 7: Return state
    return state

def generate_transaction_id():
    """Generate unique transaction ID."""
    # Format: TXN-YYYYMMDD-RANDOM
    
    date_part = datetime.now().strftime("%Y%m%d")  # 20260215
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  # A7B3C9
    return f"TXN-{date_part}-{random_part}"

def generate_booking_confirmations(flight_conf, hotel_conf, restaurant_conf):
    """Generate confirmation codes for all bookings."""
    return [
        {"type": "flight", "confirmation": flight_conf},
        {"type": "hotel", "confirmation": hotel_conf},
        {"type": "restaurant", "confirmation": restaurant_conf}
    ]

def generate_flight_confirmation(flight):
    """Generate flight confirmation code."""
    # Format: FL-{flight_id}-YYYYMMDD
    flight_id = flight['flight_id']
    date = datetime.now().strftime("%Y%m%d")
    return f"FL-{flight_id}-{date}"

def generate_hotel_confirmation(hotel):
    """Generate hotel confirmation code."""
    # Format: HT-{hotel_id}-YYYYMMDD
    hotel_id = hotel["hotel_id"]
    date = datetime.now().strftime("%Y%m%d")
    return f"HT-{hotel_id}-{date}"

def generate_restaurant_confirmation(restaurant):
    """Generate restaurant confirmation code."""
    # Format: RS-{restaurant_id}-YYYYMMDD
    restaurant_id = restaurant["restaurant_id"]
    date = datetime.now().strftime("%Y%m%d")
    return f"RS-{restaurant_id}-{date}"

if __name__ == "__main__":
    # Test case 1: Low risk (normal transaction)
    test_state = AgentState(
        user_request="Book me a trip to Miami in less than $6000",
        user_id="ksm_124"
    )
    
    state_after_planning = planning_node(test_state)
    
    state_after_research = research_node(state_after_planning)
    
    state_after_optimization = optimization_node(state_after_research)
    
    state_after_risk = risk_node(state_after_optimization)

    final_state = payment_node(state_after_risk)
    
    print("=" * 60)
    print("Payment TEST")
    print("=" * 60)
    
    print(f"Payment Status: {final_state.payment_status}")
    print(f"Transaction id: {final_state.transaction_id}")
    print(f"Payment Timestamp: {final_state.payment_timestamp}")
    print(f"Booking Confirmations: {final_state.booking_confirmations}")
    