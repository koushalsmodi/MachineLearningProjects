# Output: "Linda, welcome to the system! You are 31 years old! You have skills in: Python, MachineLearning, and LangGraph"

# name, age, skills, final

from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int 
    skills: List[str]
    final: str 
    
def first_node(state: AgentState) -> AgentState:
    """ Greets the user with a welcome message """
    state['final'] = f"{state['name']}, welcome to the system! "
    return state

def second_node(state: AgentState) -> AgentState:
    """ Adds age description to the previous state """
    state['final'] = state['final'] + f"You are {state['age']} years old! "
    return state

def third_node(state: AgentState) -> AgentState:
    """ Adds skills information to the previous state """
    state['final'] = state['final'] + f"You have skills in: {', '.join(state['skills'])}"
    return state
    
graph = StateGraph(AgentState)
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)
graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.set_finish_point("third_node")

app = graph.compile()

# display
png_bytes = app.get_graph().draw_mermaid_png()

with open("agent3_exercise_graph.png", "wb") as f:
    f.write(png_bytes)

print("✅ Graph saved as agent3_exercise_graph.png")

answer = app.invoke({"name": "Linda", "age": 31, "skills": ["Python, Machine Learning, and LangGraph"]})
print(answer['final'])