# {'name': 'Alex', 'age': '24', 'final': 'Hi Alex! You are 24 years old!'}

from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int 
    final: str 
    
def first_node(state: AgentState) -> AgentState:
    """ Takes in and returns name """
    state['final'] = f"Hi {state['name']}! "
    return state

def second_node(state: AgentState) -> AgentState:
    """ Adds and Returns age to the previous state """
    state['final'] = state['final'] + f"You are {state['age']} years old!"
    return state
graph =  StateGraph(AgentState)
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.set_finish_point("second_node")

app = graph.compile()

# display
png_bytes = app.get_graph().draw_mermaid_png()

with open("agent3_intro_graph.png", "wb") as f:
    f.write(png_bytes)

print("✅ Graph saved as agent3_intro_graph.png")

answer = app.invoke({"name": "Alex", "age": 24})
print(answer['final'])