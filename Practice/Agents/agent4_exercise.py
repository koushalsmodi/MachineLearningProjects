"""
This module defines the AgentState class and functions to create a state graph
for performing arithmetic operations based on given inputs.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# start
# node1: router_one (complete)
# edge1: addition_operation_one
# edge2: subtraction_operation_one
# node2: adder_one (complete)
# node3: subtractor_one (complete)
# node4: router_two (complete)
# edge3: addition_operation_two
# edge4:subtraction_operation_two
# node5: adder_two (complete)
# node6: subtractor_two (complete)
# end
# Input: initial_state = AgentState(
#     number1=10,
#     operation="-",
#     number2=5,
#     number3=7,
#     number4=2,
#     operation2="+",
#     finalNumber=0,
#     finalNumber2=0,
# )

class AgentState(TypedDict):
    """Represents the state of the agent with numbers and operations."""
    number1: int
    operation: str
    number2: int
    number3: int
    number4: int
    operation2: str
    finalNumber: int
    finalNumber2: int

def adder_one(state: AgentState) -> AgentState:
    """ Adds number1 and number2 """
    state['finalNumber'] = state['number1'] + state['number2']
    return state

def subtractor_one(state: AgentState) -> AgentState:
    """ Subtracts number1 and number2 """
    state['finalNumber'] = state['number1'] - state['number2']
    return state

def router_node_one(state: AgentState) -> str:
    """ Decides whether to do addition or subtraction """
    if state['operation'] == "+":
        return "addition_operation_one"

    if state['operation'] == "-":
        return "subtraction_operation_one"

def adder_two(state: AgentState) -> AgentState:
    """ Adds number3 and number4 """
    state['finalNumber2'] = state['number3'] + state['number4']
    return state

def subtractor_two(state: AgentState) -> AgentState:
    """ Subtracts number3 and number4 """
    state['finalNumber2'] = state['number3'] - state['number4']
    return state

def router_node_two(state: AgentState) -> str:
    """ Decides whether to do addition or subtraction """
    if state['operation2'] == "+":
        return "addition_operation_two"

    if state['operation2'] == "-":
        return "subtraction_operation_two"

graph = StateGraph(AgentState)

graph.add_node("router_one", lambda state: state)
graph.add_node("adder_one", adder_one)
graph.add_node("subtractor_one", subtractor_one)

graph.add_edge(START, "router_one")
graph.add_conditional_edges(
    "router_one",
    router_node_one,
    {
        # Edge: Node
        "addition_operation_one": "adder_one",
        "subtraction_operation_one": "subtractor_one",
    },

)
graph.add_node("router_two", lambda state: state)
graph.add_node("adder_two", adder_two)
graph.add_node("subtractor_two", subtractor_two)
graph.add_edge("adder_one", "router_two")
graph.add_edge("subtractor_one", "router_two")
graph.add_conditional_edges(
    "router_two",
    router_node_two,
    {
        # Edge: Node
        "addition_operation_two": "adder_two",
        "subtraction_operation_two": "subtractor_two"
    }
)
graph.add_edge("adder_two", END)
graph.add_edge("subtractor_two", END)

app = graph.compile()

# display
png_bytes = app.get_graph().draw_mermaid_png()

with open("agent4_exercise_graph.png", "wb") as f:
    f.write(png_bytes)

print("✅ Graph saved as agent4_exercise_graph.png")

initial_state_1 = AgentState(number1 = 10, operation= "-", number2 = 5, number3 = 7, number4 = 2, operation2 = "+", finalNumber = 0, finalNumber2 = 0)
print(app.invoke(initial_state_1))

initial_state_2 = AgentState(number1 = 10, operation= "+", number2 = 5, number3 = 7, number4 = 2, operation2 = "-", finalNumber = 0, finalNumber2 = 0)
print(app.invoke(initial_state_2))