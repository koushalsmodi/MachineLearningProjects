# 'Hey Bob, how is your day going?'

from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str
    

def greeting_node(state: AgentState) -> AgentState:
    """ Node greets the user """
    
    state['message'] = f"Hey {state['message']}, how is your day going?"
    return state

graph = StateGraph(state_schema=AgentState)
graph.add_node("greeter", greeting_node)
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()
png_bytes = app.get_graph().draw_mermaid_png()

with open("agent1_intro_graph.png", "wb") as f:
    f.write(png_bytes)

print("✅ Graph saved as agent1_intro_graph.png")

result = app.invoke({"message": "Bob"})
print(result['message'])