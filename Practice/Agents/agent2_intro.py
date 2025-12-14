# answers = app.invoke({"values": [1, 2, 4, 7, 19, 24], "name": "Daniel"}) 
# {'values': [1, 2, 4, 7, 19, 24], 'name': 'Daniel'}
# {'values': [1, 2, 4, 7, 19, 24], 'name': 'Daniel', 'result': 'Hi there Daniel! Your sum = 57'}

from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str 
    values: List[int]
    result: str
    
def calculator_node(state: AgentState) -> AgentState:
    """ Summing all the values """
    
    state['result'] = f"Hi, there {state['name']}! Your sum = {sum(state['values'])}"
    return state

graph = StateGraph(AgentState)
graph.add_node("calculator", calculator_node)
graph.set_entry_point("calculator")
graph.set_finish_point("calculator")

app = graph.compile()

# display
png_bytes = app.get_graph().draw_mermaid_png()

with open("agent2_intro_graph.png", "wb") as f:
    f.write(png_bytes)

print("✅ Graph saved as agent2_intro_graph.png")

answer = app.invoke({"name": "Daniel", "values": [1, 2, 4, 7, 19, 24]})
print(answer['result'])