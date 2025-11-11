# goal: buy a cheap laptop and let is decide which tools to call in what order
# budget: 50

import os
from dotenv import load_dotenv
load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])
import requests
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from dataclasses import dataclass

from main import read_products, create_cart_item, create_recommendation_request

# 1. System prompt


SYSTEM_PROMPT = """
You are a product recommender and shopping assistant.
Advise the user with just one product based on user's budget and preferences
from the Mini-Shop catalog.
Output should be short and human-readable.

You have access to four tools:
- get_products: view all available products
- get_price: look up a product's price  by ID
- add_to_cart: add one best product that fits the user's budget.
- recommend: use this to ask the Claude model for suggestions.

Always stay within the budget limit stored in memory.
"""


query = "Recommend a product to buy under $100"

# 2. Creating tools

# get_products() -> calls products
@tool
def get_products() -> list[dict]:
    """Fetch the full product catalog from the Mini-shop.
    Returns a list of product dictionaries with id, name, price, description, currency, inventory, category
    """
    products = read_products()
    return products

# get_price(product_id) -> looks up price
@tool
def get_price(product_id: int) -> float | str:
    """
    Look up the price of a product by its ID
    """
    all_products = read_products()
    for product in all_products:
        if product_id == product["id"]:
            return product["price"]
    return "Product not found"
        
# add_to_cart() -> calls cart/add
@tool 
def add_to_cart(product_id, quantity):
    """ 
    Add the selected product to the shopping cart.
    Returns a confirmation string for the agent.
    """
    create_cart_item(product_id, quantity)
    return f"Added product ID: {product_id} (quantity: {quantity}) to the cart."

# recommend() -> calls / recommend
@tool
def recommend(query: str) -> str:
    """
    Use the Claude recommender to suggest the best product for the given query.
    Returns the text recommendation.
    """
    response = requests.get("http://127.0.0.1:8000/products")
    if response.status_code == 200:
        return str(response.json())
    else:
        return "Error fetching products."

# 3. Memory 
memory = {"budget": 50}

# 4. Configure a model with parameters
model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature = 0.1,
    timeout = 60,
    max_tokens = 1000
)

model_with_tools = model.bind(tools=[get_products, get_price, add_to_cart, recommend])

# 5. Define a response format
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    query: str
    best_product: str | None = None 

# 6. Add memory
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

# 6. Create and run the agent
agent = create_agent(
    model = model_with_tools,
    system_prompt = SYSTEM_PROMPT,
    response_model = ResponseFormat,
    checkpointer = checkpointer
)

response = agent.invoke(
    {
        "messages": [{"role": "user", "content": query}]
    },
    config={"configurable": {"thread_id": "session-1"}}
)

print("\nAgent Response:\n", response)
