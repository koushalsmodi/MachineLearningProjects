from state import AgentState
from tools.helpers import calculate_nights
import json

base_dir = 'data/'

def load_user_profile(user_id):
    
    with open(base_dir + 'user_profiles.json') as f:
        all_user_profiles = json.load(f)
    
    for customer in all_user_profiles["customers"]:
        if customer["customer_id"] == user_id:
            return customer
    
    return None

def load_card_benefits(card_type):
    
    with open(base_dir + 'card_benefits.json') as f:
        card_benefits = json.load(f)
    
    return card_benefits.get(card_type)
                    
def load_amex_offers():

    with open(base_dir + 'amex_offers.json') as f:
        amex_offers = json.load(f)
    
    return amex_offers["offers"]

def score_flight(flight, user, card_benefits, amex_offers):
    total_score  = 0
    
    # Price factor (40 points max)
    max_price = 1000
    price_score = ((max_price - flight["price"]) / max_price) * 40
    total_score += price_score
    
    # cheaper better
    # Add price_score to total score
    
    max_duration= 600
    duration_score = ((max_duration - flight["duration_minutes"]) / max_duration) * 40
    total_score += duration_score

    # Stops score 
    if flight["stops"] == 0:
        total_score += 15
    elif flight["stops"] == 1:
        total_score += 7
    else:
        total_score += 0
    
    # airline bonus
    if flight["airline"] in user["preferred_airlines"]:
        total_score += 10
    
    # points earning value
    # Calculate how many points this flight earns
    # Convert points to score points
    # Add to total score
    category = "flights_direct"
    multiplier = card_benefits["points_multipliers"][category]["rate"]
    points_earned = multiplier * flight["price"]
    
    # Convert to score (assume 1000 points = 10 score points)
    points_score = (points_earned / 1000) * 10
    if points_score > 10:
        points_score = 10
        
    total_score += points_score
    
    # Amex offer bonus (5 points)
    for offer in amex_offers:
        if offer["category"] in ["flights", "travel"]:
            if offer["merchant"] == flight["airline"]:
                if flight["price"] >= offer["min_spend"]:
                    total_score += 5
                    break
    return total_score
    
    
def select_best_flight(flight_options, user, card_benefits, amex_offers):
    best_flight = None
    best_score = -1
    
    for flight in flight_options:
        score = score_flight(flight, user, card_benefits, amex_offers)  
        if score > best_score:
            best_score = score
            best_flight = flight
    
    return best_flight
    
def score_hotel(hotel, user, card_benefits, amex_offers, num_nights):
    total_score = 0
    
    max_total_price = 1200  # $600/night × 2 nights
    total_hotel_cost = hotel["price_per_night"] * num_nights
    price_score = ((max_total_price - total_hotel_cost) / max_total_price) * 40
    total_score += price_score
    
    if 4.5 <= hotel["star_rating"] <= 5:
        total_score += 15
        
    elif 4 <= hotel["star_rating"] <= 4.5:
        total_score += 10
    
    elif 3.5 <= hotel["star_rating"] <= 4:
        total_score += 7
        
    else:
        total_score += 0
    
    if hotel["chain"] in user["preferred_hotel_chains"]:
        total_score += 10
    
    category = "hotels_amex_travel"
    multiplier = card_benefits["points_multipliers"][category]["rate"]
    
    points_earned = multiplier * total_hotel_cost
    
    # Convert to score (assume 1000 points = 10 score points)
    points_score = (points_earned / 1000) * 10
    if points_score > 10:
        points_score = 10
        
    total_score += points_score
    
    for offer in amex_offers:
        if offer["category"] == "hotel":
            if offer["merchant"] == hotel["chain"]:
                if total_hotel_cost >= offer["min_spend"]:
                    total_score += 5
                    break  
    return total_score
    
def select_best_hotel(hotel_options, user, card_benefits, amex_offers, num_nights):
    best_hotel = None
    best_score = -1
    
    for hotel in hotel_options:
        score = score_hotel(hotel, user, card_benefits, amex_offers, num_nights)  
        if score > best_score:
            best_score = score
            best_hotel = hotel
    
    return best_hotel

def score_restaurant(restaurant, card_benefits, amex_offers):
    total_score = 0
    
    # based on food cost
    max_price = 200
    price_score = ((max_price - restaurant["avg_cost_per_person"]) / max_price) * 40
    total_score += price_score
    
    if 4.5 <= restaurant["rating"] <= 5:
        total_score += 15
        
    elif 4 <= restaurant["rating"] <= 4.5:
        total_score += 10
    
    elif 3.5 <= restaurant["rating"] <= 4:
        total_score += 7
        
    else:
        total_score += 0
    
    category = "restaurants"
    multiplier = card_benefits["points_multipliers"][category]["rate"]
    
    points_earned = multiplier * restaurant["avg_cost_per_person"]
    
    # Convert to score (assume 1000 points = 10 score points)
    points_score = (points_earned / 1000) * 10
    if points_score > 10:
        points_score = 10
    
    total_score += points_score
    
    for offer in amex_offers:
        if offer["category"] == "dining":
            if offer["merchant"] == restaurant["name"]:
                if  restaurant["avg_cost_per_person"] >= offer["min_spend"]:
                    total_score += 5
                    break  
    
    return total_score


def select_best_restaurant(restaurant_options, card_benefits, amex_offers):
    best_restaurant = None
    best_score = -1
    
    for restaurant in restaurant_options:
        score = score_restaurant(restaurant, card_benefits, amex_offers)
        if score > best_score:
            best_score = score
            best_restaurant = restaurant
    
    return best_restaurant

def calculate_points(selected_flight, selected_hotel, selected_restaurant, card_benefits, applied_offers, num_nights):
    total_points = 0
    
    # Flight points
    if "flights_direct" in card_benefits["points_multipliers"]:
        flight_multiplier = card_benefits["points_multipliers"]["flights_direct"]["rate"]
        total_points += selected_flight["price"] * flight_multiplier
        
    # Hotel points
    if "hotels_amex_travel" in card_benefits["points_multipliers"]:
        hotel_multiplier = card_benefits["points_multipliers"]["hotels_amex_travel"]["rate"]
        total_points += selected_hotel["price_per_night"] * hotel_multiplier * num_nights
        
    # Restaurant points
    if "restaurants" in card_benefits["points_multipliers"]:
        restaurant_multiplier = card_benefits["points_multipliers"]["restaurants"]["rate"]
        total_points += selected_restaurant["avg_cost_per_person"] * restaurant_multiplier
    
    for offer in applied_offers:
        if offer["discount_type"] == "bonus_points":
            total_points += offer["discount_value"]
    return int(total_points)

def apply_offers(selected_flight, selected_hotel, selected_restaurant, amex_offers, num_nights):
    """Check for applicable offers and calculate discount."""
    applied_offers = []
    total_discount = 0.0
    
    # Check airline offers
    flight_cost = selected_flight["price"]
    for offer in amex_offers:
        if offer["category"] in ["flights", "travel"]:
            if offer["merchant"] == selected_flight["airline"] or offer["merchant"] == "Amex Travel":
                if flight_cost >= offer["min_spend"]:
                    applied_offers.append(offer)
                    if offer["discount_type"] == "statement_credit":
                        total_discount += offer["discount_value"]
                    break
                
    # Check hotel offers
    total_hotel_cost = selected_hotel["price_per_night"] * num_nights
    for offer in amex_offers:
        if offer["category"] == "hotel":
            if offer["merchant"] == selected_hotel["chain"]:
                if total_hotel_cost >= offer["min_spend"]:
                    applied_offers.append(offer)
                    total_discount += offer["discount_value"]
                    break
    
    # Check dining offers
    restaurant_cost = selected_restaurant["avg_cost_per_person"]
    for offer in amex_offers:
        if offer["category"] == "dining":
            # "All Restaurants" or specific merchant
            if offer["merchant"] == "All Restaurants" or offer["merchant"] == selected_restaurant["name"]:
                if restaurant_cost >= offer["min_spend"]:
                    applied_offers.append(offer)
                    # Handle percentage vs fixed discount
                    if offer["discount_type"] == "percentage":
                        discount = (restaurant_cost * offer["discount_value"] / 100)
                        # Cap at max_benefit
                        discount = min(discount, offer["max_benefit"])
                    else:
                        discount = offer["discount_value"]
                    total_discount += discount
                    break
    
    return applied_offers, total_discount
    
    
def optimization_node(state: AgentState) -> AgentState:
    """Select best options and apply Amex benefits."""
    
    # 1. Load data
    user = load_user_profile(state.user_id)
    card_benefits = load_card_benefits(user["card_type"])
    amex_offers = load_amex_offers()
    
    # 2. Select best flight
    selected_flight = select_best_flight(
        state.flight_options, 
        user,
        card_benefits,
        amex_offers
    )
    
    # 3. Select best hotel
    num_nights = calculate_nights(state.travel_dates)
    selected_hotel = select_best_hotel(
        state.hotel_options,
        user,
        card_benefits,
        amex_offers,
        num_nights
    )
    
    # 4. Select best restaurant
    selected_restaurant = select_best_restaurant(
        state.restaurant_options,
        card_benefits,
        amex_offers
    )
    
    # 5. Apply offers
    applied_offers, discount = apply_offers(
        selected_flight,
        selected_hotel,
        selected_restaurant,
        amex_offers,
        num_nights
    )
    
    # 6. Calculate points earned
    
    points = calculate_points(
        selected_flight, 
        selected_hotel, 
        selected_restaurant,
        card_benefits, 
        applied_offers,
        num_nights
    )

    

    
    # 7. Calculate costs
    original_cost = (
        selected_flight["price"] + 
        selected_hotel["price_per_night"] * num_nights +
        selected_restaurant["avg_cost_per_person"]
    )
    final_cost = original_cost - discount
    
    # 8. Update state
    state.selected_flight = selected_flight
    state.selected_hotel = selected_hotel
    state.selected_restaurant = selected_restaurant
    state.applied_offers = applied_offers
    state.points_earned = points
    state.original_cost = original_cost
    state.final_cost = final_cost
    
    return state

if __name__ == "__main__":
    # Test loading
    user = load_user_profile("ksm_124")
    print("User loaded:", user["cardmember"]["firstName"], user["card_type"])
    
    benefits = load_card_benefits(user["card_type"])
    print("Card benefits loaded:", benefits["points_multipliers"]["flights_direct"])
    
    offers = load_amex_offers()
    print(f"Found {len(offers)} Amex offers")
    print("  First offer:", offers[0]["description"])