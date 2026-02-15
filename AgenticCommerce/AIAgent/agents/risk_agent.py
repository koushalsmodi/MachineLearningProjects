from state import AgentState
import json

base_dir = 'data/'

def load_user_profile(user_id):
    
    with open(base_dir + 'user_profiles.json') as f:
        all_user_profiles = json.load(f)
    
    for customer in all_user_profiles["customers"]:
        if customer["customer_id"] == user_id:
            return customer
    
    return None

def risk_node(state: AgentState) -> AgentState:
    """ 

    Input: user
    #  "remaining_credit_limit": 2000,
    # "monthly_spending_limit": 10000,
    # "past_destinations": ["San Francisco", "New York", "Mumbai"],
    # "average_transaction_amount": 1000.0,
        
    """
    
    # 1. Load user data
    user = load_user_profile(state.user_id)
    
    # 2. Amount risk
    amount_risk_score, amount_risk_reason = assess_amount_risk(state.final_cost, user)
    
    # 3. Credit risk
    credit_score, credit_reason = assess_credit_risk(state.final_cost, user)
    
    # 4. Destination risk
    destination_score, destination_reason = assess_destination_risk(state.destination, user)
    
    # 5. Pattern risk
    pattern_score, pattern_reason = assess_pattern_risk(user)
    
    # 6. Risk analysis
    risk_analysis = [
        {
            "factor": "transaction_amount",
            "score": amount_risk_score,
            "reason": amount_risk_reason
        },
        {
            "factor": "credit_utilization",
            "score": credit_score,
            "reason": credit_reason
        },
        {
            "factor": "destination",
            "score": destination_score,
            "reason": destination_reason
        },
        {
            "factor": "spending_pattern",
            "score": pattern_score,
            "reason": pattern_reason
        }
    ]
    
    # 7. Total risk_score
    
    risk_score = total_risk_score(amount_risk_score, credit_score, destination_score, pattern_score)
    
    # 8. Generate risk flags
    risk_flags = generate_risk_flags(risk_analysis, risk_score)
    
    
    # 9. Requires approval
    requires_approval = risk_score > 0.6
    
    # 10. Update state
    state.risk_score = risk_score
    state.risk_flags = risk_flags
    state.requires_approval = requires_approval
    state.risk_analysis = risk_analysis
    
    return state

def assess_amount_risk(final_cost, user):
    """ 
    Logic: Compare transaction amount to user's average_transaction_amount
    Returns: (score, reason) tuple
    Scoring:

    2x+ average -> 30 points
    1.5-2x average -> 20 points
    1.2-1.5x average -> 10 points
    < 1.2x average -> 0 points
    
    """
    amount_risk_score = 0
    amount_risk_reason = ""
    
    # risk rating
    average = user["average_transaction_amount"]
    
    if final_cost >= 2*average:
        amount_risk_score += 30
        amount_risk_reason = "Cost is 2x+ average"
        
    
    elif 1.5 *average <= final_cost < 2*average:
        amount_risk_score += 20
        amount_risk_reason = "Cost is 1.5-2x average"
    
    elif 1.2 *average <= final_cost < 1.5 *average:
        amount_risk_score += 10
        amount_risk_reason = "Cost is 1.2-1.5x average"
    
    else:
        amount_risk_score = 0
        amount_risk_reason = "Cost is < 1.2x average"
    
    
    return amount_risk_score, amount_risk_reason

def assess_credit_risk(final_cost, user):
    """ 
    Logic: Calculate what % of remaining credit this uses
    Returns: (score, reason) tuple
    Scoring:

    80% utilization -> 25 points

    50-80% utilization -> 15 points
    < 50% utilization -> 0 points
    """
    credit_score = 0
    credit_reason = ""
    
    remaining_credit = user["remaining_credit_limit"]
    
    if final_cost >= .8*remaining_credit:
        credit_score += 25
        credit_reason = "Final cost is 80% utilization of remaining credit"
    
    elif .5*remaining_credit <= final_cost < .8*remaining_credit:
        credit_score += 15
        credit_reason = "Final cost is 50-80% utilization of remaining credit"
    
    else:
        credit_score = 0
        credit_reason = "Final cost is < 50% utilization of remaining credit"
        
    return credit_score, credit_reason
    

def assess_destination_risk(destination, user):
    """ 
    Logic: Check if city is in user's past_destinations
    Returns: (score, reason) tuple
    Scoring:

    New destination -> 10 points
    Previously visited -> 0 points
    """

    destination_score = 0
    destination_reason = ""
    city = destination.split(",")[0].strip()
    past_destinations = user["past_destinations"]
    
    if city not in past_destinations:
        destination_score += 10
        destination_reason = "New destination"
    
    
    else:
        destination_score = 0
        destination_reason = "Previously visited"
        
    return destination_score, destination_reason

def assess_pattern_risk(user):
    """ 
    Logic: Is "travel" in user's typical_categories?
    Returns: (score, reason) tuple
    Scoring:

    Travel not typical -> 10 points
    Travel is typical -> 0 points
    """
    pattern_score = 0
    pattern_reason = ""
    typical_catgs = user["typical_categories"]
    
    if "travel" not in user["typical_categories"]:
        pattern_score += 10
        pattern_reason = "Travel not typical"
    
    else:
        pattern_score = 0
        pattern_reason = "Travel is typical"
        
    return pattern_score, pattern_reason

def total_risk_score(amount_risk_score, credit_score, destination_score, pattern_score):
    total_risk_score = 0
    
    total_risk_score = amount_risk_score + credit_score + destination_score + pattern_score
    total_risk_score = min(total_risk_score / 100, 1.0)
    
    return total_risk_score

def generate_risk_flags(risk_analysis, risk_score):
    """" Generate list of risk flag strings based on analysis."""
    flags = []
    
    for analysis in risk_analysis:
        factor = analysis["factor"]
        score = analysis["score"]
        
        # Amount risk flags
        if factor == "transaction_amount" and score >= 20:
            flags.append("large_transaction")
            
        elif factor == "transaction_amount" and score >= 10:
            flags.append("above_average_spending")
        
        # Credit risk flags
        if factor == "credit_utilization" and score >= 20:
            flags.append("high_credit_utilization")
        
        # Destination risk flags
        if factor == "destination" and score >= 10:
            flags.append("new_destination")
        
        # Pattern risk flags
        if factor == "spending_pattern" and score >= 10:
            flags.append("unusual_category")
    
    # Overall risk flag
    if risk_score >= 0.6:
        flags.append("requires_manual_review")
    
    return flags

if __name__ == "__main__":
    # Test case 1: Low risk (normal transaction)
    test_state_low = AgentState(
        user_request="Book me a trip to Miami",
        user_id="ksm_124",
        final_cost=760.0,  # Close to user's average
        destination="Miami, Florida"  # Previously visited
    )
    
    result_low = risk_node(test_state_low)
    print("=" * 60)
    print("LOW RISK TEST")
    print("=" * 60)
    print(f"Risk Score: {result_low.risk_score:.2f}")
    print(f"Requires Approval: {result_low.requires_approval}")
    print(f"Risk Flags: {result_low.risk_flags}")
    print("\nRisk Analysis:")
    for item in result_low.risk_analysis:
        print(f"  {item['factor']}: {item['score']} - {item['reason']}")
    
    # Test case 2: High risk (large + new destination)
    test_state_high = AgentState(
        user_request="Book me an expensive trip to Tokyo",
        user_id="ksm_124",
        final_cost=6000.0,  # 2.5x average!
        destination="Tokyo, Japan"  # New destination
    )
    
    result_high = risk_node(test_state_high)
    print("\n" + "=" * 60)
    print("HIGH RISK TEST")
    print("=" * 60)
    print(f"Risk Score: {result_high.risk_score:.2f}")
    print(f"Requires Approval: {result_high.requires_approval}")
    print(f"Risk Flags: {result_high.risk_flags}")
    print("\nRisk Analysis:")
    for item in result_high.risk_analysis:
        print(f"  {item['factor']}: {item['score']} - {item['reason']}")