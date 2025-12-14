# "Bob , you're doing an amazing job learning LangGraph!"

from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    messages: str 
    
def compliment_node(state: AgentState) -> AgentState:
    """ Compliment a user for learning LangGraph """
    
    state['messages'] = f"{state['messages']}, you're doing an amazing job learning LangGraph!"
    return state 

graph = StateGraph(AgentState)
graph.add_node("complimenter", compliment_node)
graph.set_entry_point("complimenter")
graph.set_finish_point("complimenter")

app = graph.compile()

# display
png_bytes = app.get_graph().draw_mermaid_png()

with open("agent1_exercise_graph.png", "wb") as f:
    f.write(png_bytes)

print("✅ Graph saved as agent1_exercise_graph.png")



answer = app.invoke({"messages": "Bob"})
print(answer['messages'])