"""
Input: {"name": Jack Sparrow, "values": [1,2,3,4], "operation": "*"}
Output: "Hi Jack Sparrow, your answer is: 24"
"""

from typing import TypedDict, List
from langgraph.graph import StateGraph
import math

class AgentState(TypedDict):
    name: str 
    values: List[int]
    operation: str
    result: str

def calculator_node(state: AgentState) -> AgentState:
    """ Calculator that decides whether user's input is * or + and takes actions accordingly """

    if state['operation'] == "+":
        state['result'] = f"Hi {state['name']}, your answer is: {sum(state['values'])}"
    
    if state['operation'] == "*":
        state['result'] = f"Hi {state['name']}, your answer is: {math.prod(state['values'])}"   
    
    return state   

graph = StateGraph(AgentState)
graph.add_node("calculator", calculator_node)
graph.set_entry_point("calculator")
graph.set_finish_point("calculator")

app = graph.compile()

# display
png_bytes = app.get_graph().draw_mermaid_png()

with open("agent2_exercise_graph.png", "wb") as f:
    f.write(png_bytes)

print("✅ Graph saved as agent2_exercise_graph.png")

answer = app.invoke({"name": "Jack Sparrow", "values": [1,2,3,4], "operation": "*"})
print(answer['result'])

answer_2 = app.invoke({"name": "Jack Sparrow", "values": [1,2,3,4], "operation": "+"})
print(answer_2['result'])