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
Output 1:
(venv) (base) koushalsmodi@Koushals-MacBook-Pro mini-shop-api % python3 agent_runner.py
API key loaded: sk-ant-api
API key loaded: sk-ant-api

=== Starting Agent ===

Iteration 1
2025-11-11 19:17:26,848 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: recommend with args: {'user_query': 'best product under $500 budget'}
2025-11-11 19:17:31,787 - INFO - Tool called: recommend(user_query)
Tool result: Based on your $500 budget, I recommend:

**HP Spectre - $249**
- Great laptop option well within your budget
- Leaves you with $251 to spare
- In stock with 40 units available

This is the perfect choice for you as the Apple MacBook at $2,000 exceeds your budget. The HP Spectre offers solid performance and value at less than half your budget!

Iteration 2
2025-11-11 19:17:34,937 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: add_to_cart with args: {'product_id': 2, 'quantity': 1}
2025-11-11 19:17:34,953 - INFO - Attempt to add 2 X qty 1 subtotal: $249.0 - within budget - added
Tool result: Added product ID: 2 (quantity: 1) to the cart.

Iteration 3
2025-11-11 19:17:37,089 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: checkout with args: {}
2025-11-11 19:17:37,110 - INFO - Tool called: checkout()
Tool result: Purchase confirmed. Order placed successfully.

Iteration 4
2025-11-11 19:17:41,388 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"

=== Final Response ===
Great! I've successfully:
✅ Recommended the **HP Spectre laptop** for $249 - perfect for your $500 budget
✅ Added it to your cart
✅ Completed your purchase

Your order is confirmed! You saved $251 from your budget and got a quality laptop. Thank you for shopping with us!
"""


""" 
Output 2:
(venv) (base) koushalsmodi@Koushals-MacBook-Pro mini-shop-api % python3 agent_runner.py
API key loaded: sk-ant-api
API key loaded: sk-ant-api

=== Starting Agent ===

Iteration 1
2025-11-11 19:19:04,849 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: recommend with args: {'user_query': 'best product under $500 budget'}
2025-11-11 19:19:11,837 - INFO - Tool called: recommend(user_query)
Tool result: Based on your $500 budget, here are my recommendations:

**Best Options:**

1. **HP Spectre** - $249
   - Great mid-range laptop with excellent features
   - Well within your budget, leaving you $251 to spare

2. **Dell Alienware** - $111
   - Budget-friendly option
   - Leaves plenty of room in your budget for accessories

Both are solid choices under $500. The **HP Spectre at $249** offers the best value if you want to invest more in quality, while the **Dell Alienware at $111** is perfect if you want to save money.

*Note: The Apple Macbook ($2000) exceeds your budget.*

Would you like more details about either option?

Iteration 2
2025-11-11 19:19:15,028 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: add_to_cart with args: {'product_id': 2, 'quantity': 1}
2025-11-11 19:19:15,045 - INFO - Attempt to add 2 X qty 1 subtotal: $249.0 - within budget - added
Tool result: Added product ID: 2 (quantity: 1) to the cart.

Iteration 3
2025-11-11 19:19:18,468 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: checkout with args: {}
2025-11-11 19:19:18,490 - INFO - Tool called: checkout()
Tool result: Purchase confirmed. Order placed successfully.

Iteration 4
2025-11-11 19:19:22,256 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"

=== Final Response ===
✅ **Order Complete!**

I've successfully recommended and purchased the **HP Spectre laptop for $249** - a great mid-range laptop that fits well within your $500 budget. Your order has been placed and confirmed.

You saved $251 from your budget while getting an excellent quality laptop. Enjoy your new HP Spectre!
"""