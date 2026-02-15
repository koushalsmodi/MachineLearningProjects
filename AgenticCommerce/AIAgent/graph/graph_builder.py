from state import AgentState  # ← Import your existing state
from agents.planning_agent import planning_node
from agents.research_agent import research_node
from agents.optimization_agent import optimization_node
from agents.risk_agent import risk_node
from agents.payment_agent import payment_node
from agents.confirmation_agent import confirmation_node
from langgraph.graph import StateGraph, START, END

def human_approval_node(state: AgentState) -> AgentState:
    """Human approval gate for high-risk transactions."""
    
    print(f"Risk Score: {state.risk_score}")
    print(f"Risk Flags: {state.risk_flags}")
    print(f"Transaction Amount: ${state.final_cost}")
    
    # Get human decision
    approval = input("Approve this transaction? (y/n): ")
    
    if approval.lower() == 'y':
        print("✅ Transaction approved by human reviewer")
        # State continues to payment
    else:
        print("❌ Transaction rejected by human reviewer")
        state.payment_status = "rejected_by_reviewer"
    
    return state
    

def route_after_risk(state: AgentState):
    """Decide path after risk assessment."""
    if state.requires_approval:
        return "human_approval"  
    else:
        return "payment"
    

def create_booking_graph():
    """Create and compile the booking workflow graph."""
    
    # Create graph using your existing AgentState
    graph = StateGraph(AgentState)
    
    # Add all nodes
    graph.add_node("planning", planning_node)
    graph.add_node("research", research_node)
    graph.add_node("optimization", optimization_node)
    graph.add_node("risk", risk_node)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("payment", payment_node)
    graph.add_node("confirmation", confirmation_node)
    
    # Add sequential edges
    graph.add_edge(START, "planning")
    graph.add_edge("planning", "research")
    graph.add_edge("research", "optimization")
    graph.add_edge("optimization", "risk")
    
    # Add conditional edge (risk → approval or payment)
    graph.add_conditional_edges(
        "risk",
        route_after_risk,
        {
            "human_approval": "human_approval",
            "payment": "payment"
        }
    )
    
    # Continue from approval to payment
    graph.add_edge("human_approval", "payment")
    
    # Final edges
    graph.add_edge("payment", "confirmation")
    graph.add_edge("confirmation", END)
    
    # Compile and return
    final_graph = graph.compile()
    return final_graph
    
    
if __name__ == "__main__":
    initial_state = AgentState(
        user_request="Book me a trip to Miami for weekend in less than $6000",
        user_id="ksm_124"
    )
    
    print("="*60)
    print("RUNNING BOOKING GRAPH")
    print("="*60)
    
    graph = create_booking_graph()
    final_state = graph.invoke(initial_state) 
    
    # Print final confirmation
    print("\n" + "="*60)
    print("BOOKING COMPLETE")
    print("="*60)
    print(final_state['confirmation_message'])
    