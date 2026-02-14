from state import AgentState
from agents.planning_agent import planning_node
from agents.research_agent import research_node
from agents.optimization_agent import optimization_node

# Create initial state
initial_state = AgentState(
    user_request="Book me a trip to Miami for the weekend under $2000",
    user_id="ksm_124"
)

print("=" * 60)
print("STEP 1: PLANNING AGENT")
print("=" * 60)

# Run planning agent
state_after_planning = planning_node(initial_state)
print(f"Destination: {state_after_planning.destination}")
print(f"Budget: ${state_after_planning.budget}")
print(f"Preferences: {state_after_planning.preferences}")

print("\n" + "=" * 60)
print("STEP 2: RESEARCH AGENT")
print("=" * 60)

# Run research agent
state_after_research = research_node(state_after_planning)
print(f"Found {len(state_after_research.flight_options)} flights")
print(f"Found {len(state_after_research.hotel_options)} hotels")
print(f"Found {len(state_after_research.restaurant_options)} restaurants")

print("\n" + "=" * 60)
print("STEP 3: OPTIMIZATION AGENT")
print("=" * 60)

# Run optimization agent
final_state = optimization_node(state_after_research)

# Print results
print(f"\n✈️ SELECTED FLIGHT:")
print(f"   {final_state.selected_flight['airline']} - ${final_state.selected_flight['price']}")
print(f"   {final_state.selected_flight['origin']} → {final_state.selected_flight['destination']}")
print(f"   Duration: {final_state.selected_flight['duration_minutes']} mins, Stops: {final_state.selected_flight['stops']}")

print(f"\n🏨 SELECTED HOTEL:")
print(f"   {final_state.selected_hotel['name']} ({final_state.selected_hotel['chain']})")
print(f"   ${final_state.selected_hotel['price_per_night']}/night × {len(final_state.travel_dates) if final_state.travel_dates else 1} nights")
print(f"   ⭐ {final_state.selected_hotel['star_rating']} stars, {final_state.selected_hotel['location_type']}")

print(f"\n🍽️ SELECTED RESTAURANT:")
print(f"   {final_state.selected_restaurant['name']} ({final_state.selected_restaurant['cuisine_type']})")
print(f"   ${final_state.selected_restaurant['avg_cost_per_person']}/person")
print(f"   ⭐ {final_state.selected_restaurant['rating']}, {final_state.selected_restaurant['price_range']}")

print(f"\n💰 COST BREAKDOWN:")
print(f"   Original Cost: ${final_state.original_cost:.2f}")
if final_state.applied_offers:
    print(f"   Applied Offers:")
    for offer in final_state.applied_offers:
        print(f"      - {offer['description']}")
print(f"   Final Cost: ${final_state.final_cost:.2f}")
print(f"   💵 You Saved: ${final_state.original_cost - final_state.final_cost:.2f}")

print(f"\n🎁 REWARDS:")
print(f"   Points Earned: {final_state.points_earned:,} points")

print("\n" + "=" * 60)