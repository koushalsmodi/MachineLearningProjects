# start, greeting
# random: loop or exit -> end
# app.invoke({"name": "Neeshaa Modii", "number": [], "counter": -1})
# {'name': 'Hi there, Neeshaa Modii', 'number': [1, 3, 1, 1, 8], 'counter': 5}

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END 
import random

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int 

def greeting_node(state: AgentState) -> AgentState:
    """ Greeting the user """
    state['name'] = f"Hi there, {state['name']}"
    state['counter'] = 0
    return state 

def random_node(state: AgentState) -> AgentState:
    """ Generating random numbers """
    num = random.randint(0, 10)
    state['counter'] += 1
    state['number'].append(num)
    return state

def decision_node(state: AgentState) -> AgentState:
    """ Deciding whether or not to loop """
    
    if state['counter'] < 5:
        print('ENTERING LOOP', state['counter'])
        return "loop"

    else:
        return "exit"


graph = StateGraph(AgentState)
graph.add_node("greeting_node", greeting_node)
graph.add_node("random_node", random_node)
graph.add_edge("greeting_node", "random_node")
graph.add_conditional_edges(
    "random_node",
    decision_node,
    {
        # Edge: Node
        "loop": "random_node",
        "exit": END
    }
)
graph.set_entry_point("greeting_node")
app = graph.compile()

# display
png_bytes = app.get_graph().draw_mermaid_png()

with open("agent5_intro_graph.png", "wb") as f:
    f.write(png_bytes)

print("✅ Graph saved as agent5_intro_graph.png")

answer = app.invoke({"name": "Neeshaa Modii", "number": [], "counter": -1})
print(answer)