import os
import requests
import logging
from dotenv import load_dotenv
from langchain.tools import tool
from memory_store import memory

load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])

from langchain_anthropic import ChatAnthropic

from main import products

logging.basicConfig(
    filename = "logs/mini_shop.log",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s  - %(message)s"
)

# 1. System prompt
SYSTEM_PROMPT = """
You are a product recommender and shopping assistant.
Advise the user with just one product based on user's budget and preferences
from the Mini-Shop catalog.
Output should be short and human-readable.

The user's budget is $50.

You have access to five tools:
- get_products: view all available products
- get_price: look up a product's price by ID
- add_to_cart: add one best product that fits the user's budget
- recommend: use this to get AI recommendations
- checkout: use this confirm for purchase confirmation

Always stay within the budget limit of $50.
"""

query = "Recommend a product to buy under $50 and add it to my cart and proceed to checkout."

# 2. Creating tools (using HTTP requests to the API)
@tool
def get_products() -> list[dict]:
    """Fetch the full product catalog from the Mini-shop.
    Returns a list of product dictionaries with id, name, price, description, currency, inventory, category
    """
    try:
        response = requests.get("http://127.0.0.1:8000/products")
        logging.info("Tool called: get_products()")
        if response.status_code == 200:
            return response.json()
            logging.info("Tool result: {len(products)} items retrieved")
        return []
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []

@tool
def get_price(product_id: int) -> float | str:
    """Look up the price of a product by its ID"""
    try:
        response = requests.get("http://127.0.0.1:8000/products")
        logging.info("Tool called: getprice(product_id)")
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
        logging.info("Tool called: add_to_cart(product_id, quantity)")
        
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
        logging.info("Tool called: recommend(user_query)")
        if response.status_code == 200:
            data = response.json()
            return data.get("recommendation", "No recommendation available")
        else:
            return "Error fetching recommendation"
    except Exception as e:
        return f"Error: {e}"

@tool
def checkout() -> str:
    """Simulate completing the purchase"""
    api_key = os.getenv("API_KEY")
    headers = {"x-api-key": api_key}
    checkoutin = {
        "customer_name": "John Doe",
        "email": "john@example.com"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/checkout",
        headers=headers,
        json=checkoutin
    )
    
    logging.info("Tool called: checkouts()")
    if response.status_code == 200:
        return "Purchase confirmed. Order placed successfully."
    return f"Checkout failed: {response.text}"
    
# 3. Create tools list
tools = [get_products, get_price, add_to_cart, recommend, checkout]

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
(venv) (base) koushalsmodi@Koushals-MacBook-Pro mini-shop-api % python3 agent_tools.py
API key loaded: sk-ant-api
API key loaded: sk-ant-api

=== Starting Agent ===

Iteration 1
2025-11-11 17:58:00,255 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: recommend with args: {'user_query': 'best product under $50 budget'}
2025-11-11 17:58:04,993 - INFO - Tool called: recommend(user_query)
Tool result: Based on your $50 budget, I recommend:

**HP Spectre - $49**
- Category: Laptop
- In stock with plenty of inventory

This is the only product in our catalog that fits within your $50 budget. It's priced at $49, leaving you $1 under budget, and we have good availability with 2,000 units in stock.

Iteration 2
2025-11-11 17:58:09,265 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: add_to_cart with args: {'product_id': 1, 'quantity': 1}
2025-11-11 17:58:09,274 - INFO - Tool called: add_to_cart(product_id, quantity)
Tool result: Added product ID: 1 (quantity: 1) to the cart.

Iteration 3
2025-11-11 17:58:11,621 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
Calling tool: checkout with args: {}
2025-11-11 17:58:11,652 - INFO - Tool called: checkouts()
Tool result: Purchase confirmed. Order placed successfully.

Iteration 4
2025-11-11 17:58:15,816 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"

=== Final Response ===
Great! I've successfully:
✅ Recommended the **HP Spectre laptop** for $49 (within your $50 budget)
✅ Added it to your cart
✅ Completed your purchase

Your order has been placed successfully! You saved $1 from your budget and got a great laptop. Thank you for shopping with us!
(venv) (base) koushalsmodi@Koushals-MacBook-Pro mini-shop-api % 
"""