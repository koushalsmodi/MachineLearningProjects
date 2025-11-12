import os
import requests

from dotenv import load_dotenv
from langchain.tools import tool
from memory_store import memory

load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])

from langchain_anthropic import ChatAnthropic

from main import products

# 1. System prompt
SYSTEM_PROMPT = """
You are a product recommender and shopping assistant.
Advise the user with just one product based on user's budget and preferences
from the Mini-Shop catalog.
Output should be short and human-readable.

The user's budget is $50.

You have access to four tools:
- get_products: view all available products
- get_price: look up a product's price by ID
- add_to_cart: add one best product that fits the user's budget
- recommend: use this to get AI recommendations

Always stay within the budget limit of $50.
"""

query = "Recommend a product to buy under $50 and add it to my cart"

# 2. Creating tools (using HTTP requests to the API)
@tool
def get_products() -> list[dict]:
    """Fetch the full product catalog from the Mini-shop.
    Returns a list of product dictionaries with id, name, price, description, currency, inventory, category
    """
    try:
        response = requests.get("http://127.0.0.1:8000/products")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []

@tool
def get_price(product_id: int) -> float | str:
    """Look up the price of a product by its ID"""
    try:
        response = requests.get("http://127.0.0.1:8000/products")
        if response.status_code == 200:
            all_products = response.json()
            for product in all_products:
                if product_id == product["id"]:
                    return product["price"]
        return "Product not found"
    except Exception as e:
        return f"Error: {e}"
        
@tool 
def add_to_cart(product_id: int, quantity: int) -> str:
    """Add the selected product to the shopping cart.
    Returns a confirmation string for the agent.
    """
    try:
        api_key = os.getenv("API_KEY")
        headers = {"x-api-key": api_key}
        payload = {"product_id": product_id, "quantity": quantity}
        
        response = requests.post(
            "http://127.0.0.1:8000/cart/add",
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            return f"Added product ID: {product_id} (quantity: {quantity}) to the cart."
        else:
            return f"Failed to add to cart: {response.text}"
    except Exception as e:
        return f"Error adding to cart: {e}"

@tool
def recommend(user_query: str) -> str:
    """Use the Claude recommender to suggest the best product for the given query.
    Returns the text recommendation.
    """
    try:
        response = requests.post(
            "http://127.0.0.1:8000/recommend",
            json={"query": user_query}
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("recommendation", "No recommendation available")
        else:
            return "Error fetching recommendation"
    except Exception as e:
        return f"Error: {e}"

# 3. Create tools list
tools = [get_products, get_price, add_to_cart, recommend]

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
            
"""Output:
base) koushalsmodi@Koushals-MacBook-Pro mini-shop-api % python3 agent_tools.py         
API key loaded: sk-ant-api
API key loaded: sk-ant-api

=== Starting Agent ===

Iteration 1
2025-11-11 17:33:09,070 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: recommend with args: {'user_query': 'best product under $50 budget'}
Tool result: Based on your $50 budget, I recommend:

**HP Spectre** - $49
- Category: Laptop
- Great value right at your budget limit
- In stock with good availability

This is the only laptop option that fits within your $50 budget from our current catalog.

Iteration 2
2025-11-11 17:33:17,772 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: add_to_cart with args: {'product_id': 3, 'quantity': 1}
Tool result: Added product ID: 3 (quantity: 1) to the cart.

Iteration 3
2025-11-11 17:33:21,092 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"

=== Final Response ===
Great! I've added the **HP Spectre laptop** ($49) to your cart. It's a fantastic laptop that uses almost your entire $50 budget, leaving you with $1 to spare. This gives you excellent value for a laptop at this price point!
"""