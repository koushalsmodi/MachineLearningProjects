from langchain_anthropic import ChatAnthropic
from agent_tools import tools, SYSTEM_PROMPT, query

# 4. Configure model with tools
model = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0.1,
    timeout=60,
    max_tokens=1000
)

model_with_tools = model.bind_tools(tools)

# 5. Simple execution loop
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": query}
]

print("\n=== Starting Agent ===\n")

# Run for up to 10 iterations to handle tool calls
for i in range(10):
    print(f"Iteration {i+1}")
    response = model_with_tools.invoke(messages)
    messages.append({
        "role": "assistant", 
        "content": response.content, 
        "tool_calls": response.tool_calls if hasattr(response, 'tool_calls') else []
    })
    
    # Check if there are tool calls
    if not response.tool_calls:
        print("\n=== Final Response ===")
        print(response.content)
        break
    
    # Execute tool calls
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        print(f"Calling tool: {tool_name} with args: {tool_args}")
        
        # Find and execute the tool
        tool_func = next((t for t in tools if t.name == tool_name), None)
        if tool_func:
            result = tool_func.invoke(tool_args)
            print(f"Tool result: {result}\n")
            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_call_id": tool_call["id"]
            })
        else:
            print(f"Tool {tool_name} not found")
            
  