import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])

# Create tools
# Let's a model interact with external systems by calling functions you define.
# Tools can depend on runtime context and also interact with agent memory.
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {city}"


model = init_chat_model( 
        "claude-sonnet-4-5-20250929",
        temperature = 0.5,
        timeout = 10,
        max_tokens = 1000
    )

# Bind (potentially multiple) tools to the model
model_with_tools = model.bind_tools([get_weather])

# Step 1: Model generates tool calls
messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)

# Step 2: Execute tools and collect results
for tool_call in ai_msg.tool_calls:
    
    # Execute the tool with the generated arguments
    tool_result = get_weather.invoke(tool_call)
    messages.append(tool_result)

# Step 3: Pass results back to model for final response
final_response = model_with_tools.invoke(messages)
print(final_response.text)

# by default, model has freedom to choose which bound tool to use based on user's input,
# however, we can force choosing a tool, ensuring to have it use a particular tool or any tool from a given list

# for any tool:
# model_with_tools = model.bind_tools([tool_1], tool_choice = "any")

# for specific tools:
# model_with_tools = model.bind_tools([tool_1], tool_choice = "tool_1")

# # parallel tool calls
# model_with_tools = model.bind_tools([get_weather])
# response = model_with_tools.invoke("What's the weather in Boston and Tokyo?")

# # The model may generate multiple tool calls
# print(response.tool_calls)

# # Execute all tools (can be done in parallel with async)
# results = []
# for tool_call in response.tool_calls:
#     if tool_call['name'] == 'get_weather':
#         result = get_weather.invoke(tool_call)


# streaming tool calls
for chunk in model_with_tools.stream("What's the weather in Boston and Tokyo?"):
    # Tool call chunks arrive progressively
    for tool_chunk in chunk.tool_call_chunks:
        if name:= tool_chunk.get("name"):
            print(f"Tool: {name}")
        
        if id_:= tool_chunk.get("id"):
            print(f"ID: {id_}")
        
        if args:= tool_chunk.get("args"):
            print(f"Args: {args}")