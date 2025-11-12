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
            
            
""" 
Output:
(venv) (base) koushalsmodi@Koushals-MacBook-Pro mini-shop-api % python3 agent_runner.py 
API key loaded: sk-ant-api
API key loaded: sk-ant-api

=== Starting Agent ===

Iteration 1
2025-11-11 18:06:27,869 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: recommend with args: {'user_query': 'best product under $50 budget'}
2025-11-11 18:06:33,210 - INFO - Tool called: recommend(user_query)
Tool result: Based on your $50 budget, I recommend:

**HP Spectre - $49**
- Category: Laptop
- Well within your budget
- In stock with good availability

This is the only product in our catalog that fits your $50 budget constraint. It's priced at $49, leaving you $1 under budget!

Iteration 2
2025-11-11 18:06:36,672 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: add_to_cart with args: {'product_id': 3, 'quantity': 1}
2025-11-11 18:06:36,680 - INFO - Tool called: add_to_cart(product_id, quantity)
Tool result: Added product ID: 3 (quantity: 1) to the cart.

Iteration 3
2025-11-11 18:06:39,128 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: checkout with args: {}
2025-11-11 18:06:39,164 - INFO - Tool called: checkouts()
Tool result: Purchase confirmed. Order placed successfully.

Iteration 4
2025-11-11 18:06:42,608 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"

=== Final Response ===
Great! I've successfully:
✅ Recommended the **HP Spectre laptop** for $49 (within your $50 budget)
✅ Added it to your cart
✅ Completed your purchase

Your order has been placed successfully! You got a great laptop while staying $1 under budget. Enjoy your new HP Spectre!
"""