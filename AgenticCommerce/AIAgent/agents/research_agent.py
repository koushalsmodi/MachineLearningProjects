from state import AgentState
import json

base_dir = 'data/mock/'

def research_node(state: AgentState) -> AgentState:
    """Find flight, hotel, and restaurant options based on user criteria."""
    destination = state.destination
    travel_dates = state.travel_dates
    budget = state.budget
    preferences = state.preferences
    
    with open(base_dir + 'mock_flights.json') as f:
        all_flights = json.load(f)
    
    with open(base_dir + 'mock_hotels.json') as f:
        all_hotels = json.load(f)
    
    with open(base_dir + 'mock_restaurants.json') as f:
        all_restaurants = json.load(f)
    
    hotel_budget = budget * 0.4
    restaurant_budget = budget * 0.1
    
    matching_flights = filter_flights(all_flights, destination, budget)
    matching_hotels = filter_hotels(all_hotels, preferences, hotel_budget, travel_dates)
    matching_restaurants = filter_restaurants(all_restaurants, restaurant_budget)
    
    state.flight_options = matching_flights
    state.hotel_options = matching_hotels
    state.restaurant_options = matching_restaurants
    
    return state

def does_flight_match_destination(flight, destination):
    """ Return whether the flight reaches the destination"""
    flight_dest = flight["destination"]
    user_dest_upper = destination.upper()
    
    return flight_dest in user_dest_upper or "MIAMI" in user_dest_upper
    
    
# Helper function to filter flights
def filter_flights(all_flights, destination, budget):
    matching_flights = []
    
    for route_name in all_flights["routes"]:
        flights_in_route = all_flights["routes"][route_name]
        
        max_flight_budget = budget * 0.5  
        
        for flight in flights_in_route:
            if does_flight_match_destination(flight, destination):
                if flight["price"] <= max_flight_budget:
                    matching_flights.append(flight) 
                    
    return matching_flights


def calculate_nights(travel_dates):
    if len(travel_dates) < 2:
        nights = 1
    else:
        nights = len(travel_dates) - 1

    return nights
        
    
# Helper function to filter hotels
def filter_hotels(all_hotels, preferences, hotel_budget, travel_dates):
    matching_hotels = []
    
    if travel_dates and len(travel_dates) >= 2:
        num_nights = calculate_nights(travel_dates)
    
    else:
        num_nights = 2
    
    wants_beachfront = False
    for pref in preferences:
        pref_lower = pref.lower()
        if "beachfront" in pref_lower:
            wants_beachfront = True
            break
        
    for location in all_hotels["hotels"]:
        hotels_at_location = all_hotels["hotels"][location]
        
        for hotel in hotels_at_location:
            if wants_beachfront and hotel["location_type"] != "beachfront":
                continue
        
            total_cost = num_nights * hotel["price_per_night"]
            if total_cost <= hotel_budget:
                matching_hotels.append(hotel)
        
    return matching_hotels

# Helper function to filter restaurants
def filter_restaurants(all_restaurants, restaurant_budget):
    
    matching_restaurants = []
    
    for location in all_restaurants["restaurants"]:
        restaurants_at_location = all_restaurants["restaurants"][location]
        
        for restaurant in restaurants_at_location:
            if restaurant["reservations_available"]: 
                if restaurant["avg_cost_per_person"] <= restaurant_budget:
                    matching_restaurants.append(restaurant)
                
    return matching_restaurants
    

if __name__ == "__main__":
    test_state = AgentState(
        user_request= "Book me a trip to Miami for the weekend in less than $2000",
        user_id = "ksm_124",
        destination = "Miami, FL",
        travel_dates = ["2026-03-30", "2026-03-31"],
        budget = 2000.0,
        preferences = ["beachfront"]
    )
    updated_state = research_node(test_state)
    
    print(f"Updated State: {updated_state}")
    
    print("\n")
    print(f"Found {len(updated_state.flight_options)} flights")
    print(f"Found {len(updated_state.hotel_options)} hotels")
    print(f"Found {len(updated_state.restaurant_options)} restaurants")
    
    if updated_state.flight_options:
        print("\nSample flight:", updated_state.flight_options[0]["airline"], 
              "-", updated_state.flight_options[0]["price"])
        
    if updated_state.hotel_options:
        print("Sample hotel:", updated_state.hotel_options[0]["name"], 
              "-", updated_state.hotel_options[0]["price_per_night"])
        
    if updated_state.restaurant_options:
        print("Sample restaurant:", updated_state.restaurant_options[0]["name"], 
              "-", updated_state.restaurant_options[0]["avg_cost_per_person"])