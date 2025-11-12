import os
import requests
import logging
from dotenv import load_dotenv
from langchain.tools import tool
from memory_store import memory

load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])

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

The user's budget is $memory['budget'].

You have access to five tools:
- get_products: view all available products
- get_price: look up a product's price by ID
- add_to_cart: add one best product that fits the user's budget
- recommend: use this to get AI recommendations
- checkout: use this confirm for purchase confirmation

Always stay within the budget limit of $memory['budget'].
"""

query = "Recommend a product to buy under $memory['budget'] and add it to my cart and proceed to checkout."

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
        price = get_price(product_id)
        
        subtotal = price * quantity
        if subtotal <= memory["budget"]:
            response = requests.post(
                "http://127.0.0.1:8000/cart/add",
                json=payload,
                headers=headers
            )
            logging.info("Tool called: add_to_cart(product_id, quantity)")
        
            if response.status_code == 200:
                return f"Added product ID: {product_id} (quantity: {quantity}) to the cart."
                logging.info(f"Attempt to add {product_id} X qty {quantity} subtotal: ${subtotal} - within budget - added")
            
            else:
                return f"Failed to add to cart: {response.text}"
        else:
            return f"Price exceeded the user budget {memory['budget']}"
        logging.error(f"Price exceeded the user budget {memory['budget']}")
        
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