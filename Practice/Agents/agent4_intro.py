# Conditional edges

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int 
    number2: int 
    operation: str 
    finalNumber: int
    

def add_node(state: AgentState) -> AgentState:
    """ Adding two numbers """
    state['finalNumber'] = state['number1'] + state['number2']
    return state

def subtract_node(state: AgentState) -> AgentState:
    """ Subtrating the two numbers """
    state['finalNumber'] = state['number1'] - state['number2']
    return state 

def decide_next_node(state: AgentState) -> AgentState:
    """ Decides whehter to call edge for add node or subtract node """
    
    if state['operation'] == "+":
        return "add_operation"
    
    if state['operation'] == "-":
        return "subtract_operation"
    
graph = StateGraph(AgentState)
graph.add_node("add_node", add_node)
graph.add_node("subtract_node", subtract_node)
graph.add_node("router", lambda state: state)
graph.set_entry_point("router")
graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router", # source node
    decide_next_node, # path
    {
        # Edge: Node
        "add_operation": "add_node",
        "subtract_operation": "subtract_node",
    },
)
graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)

app = graph.compile()

# display
png_bytes = app.get_graph().draw_mermaid_png()

with open("agent4_intro_graph.png", "wb") as f:
    f.write(png_bytes)

print("✅ Graph saved as agent4_intro_graph.png")

answer = app.invoke({"number1": 10, "number2": 1, "operation": "+"})
print(answer['finalNumber'])  # Output: 11

answer = app.invoke({"number1": 11, "number2": 1, "operation": "-"})
print(answer['finalNumber'])  # Output: 10