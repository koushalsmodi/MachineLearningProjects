import os
import requests
import logging
from dotenv import load_dotenv
from langchain.tools import tool
from memory_store import memory

load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])

from main import products

logger = logging.getLogger(__name__)

# 1. System prompt
SYSTEM_PROMPT = f"""
You are a product recommender and shopping assistant.
Advise the user with just one product based on user's budget and preferences
from the Mini-Shop catalog.
Output should be short and human-readable.

The user's budget is ${memory['budget']}.

You have access to five tools:
- get_products: view all available products
- get_price: look up a product's price by ID
- add_to_cart: add one best product that fits the user's budget
- recommend: use this to get AI recommendations
- checkout: use this confirm for purchase confirmation

Always stay within the budget limit of ${memory['budget']}.
"""

query = f"Recommend a product to buy under ${memory['budget']} and add it to my cart and proceed to checkout."

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
            data =  response.json()
            logger.info("Tool result: {len(products)} items retrieved")
            return data 
        logger.warning(f"get_products() failed with status {response.status_code}")
        return []
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return []

# Store the original function before decorating
def _get_price_impl(product_id: int) -> float | str:
    """Implementation of get_price logic"""
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
def get_price(product_id: int) -> float | str:
    """Look up the price of a product by its ID"""
    logger.info(f"Tool called: get_price(product_id={product_id})")
    price =  _get_price_impl(product_id)
    logger.info(f"Price lookup for ID {product_id}: {price}")
    return price
        
@tool 
def add_to_cart(product_id: int, quantity: int) -> str:
    """Add the selected product to the shopping cart.
    Returns a confirmation string for the agent.
    """
    try:
        api_key = os.getenv("API_KEY")
        headers = {"x-api-key": api_key}
        payload = {"product_id": product_id, "quantity": quantity}
        
        # Use the original implementation function, not the tool wrapper
        price = _get_price_impl(product_id)
        if not isinstance(price, (int, float)):
            logger.error(f"Invalid price for product {product_id}: {price}")
            return f"Error: invalid price for product {product_id}."
        
        subtotal = price * quantity
        
        if subtotal > memory["budget"]:
            logger.warning(f"Rejected add_to_cart: subtotal ${subtotal: .2f} exceeds budget ${memory['budget']}")
            return f"Rejected: subtotal ${subtotal: .2f} exceeds budget ${memory['budget']}"

            response = requests.post("http://127.0.0.1.8000/cart/add", json = payload, headers = headers)
            
            if response.status_code == 200:
                logger.info(f"Added product {product_id} qty {quantity}, subtotal ${subtotal:.2f} within budget ${memory['budget']}")
                return f"Added product ID {product_id} (qty: {quantity}) to cart subtotal ${subtotal:.2f}."
                
            else:
                logger.error(f"add_to_cart failed with status {response.status_code}: {response.text}")
                return f"Failed to add to cart: {response.text}"


    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        return f"Error adding to cart: {e}"

@tool
def recommend(user_query: str) -> str:
    """Use Claude recommender to suggest the best product for the given query.
    Returns the text recommendation.
    """
    try:
        response = requests.post(
            "http://127.0.0.1:8000/recommend",
            json={"query": user_query}
        )
        logger.info("Tool called: recommend(user_query)")
        
        if response.status_code == 200:
            data = response.json()
            rec =  data.get("recommendation", "No recommendation available")
            logger.info(f"Recommendation result: {rec[:70]}...")
            return rec
        
        logger.error(f"Recommend failed with status {response.status_code}")
        return "Error fetching recomendation"

    except Exception as e:
        logger.error(f"Error in recommend: {e}")
        return f"Error: {e}"

@tool
def checkout() -> str:
    """Simulate completing the purchase"""
    try:
        api_key = os.getenv("API_KEY")
        headers = {"x-api-key": api_key}
        checkoutin = {
            "customer_name": "John Doe",
            "email": "john@example.com"
        }
        
        logger.info("Tool called: checkout()")
        response = requests.post(
            "http://127.0.0.1:8000/checkout",
            headers=headers,
            json=checkoutin
        )
        
        
        if response.status_code == 200:
            logger.info(f"Checkout successful for {checkoutin['email']}")
            return "Purchase confirmed. Order placed successfully."
        
        else:
            logger.error(f"Checkout failed: {response.status_code} {response.text}")
            return f"Checkout failed: {response.text}"
    
    except Exception as e:
        logger.error(f"Error in checkout: {e}")
        return f"Error during checkout: {e}"
    

    
# 3. Create tools list
tools = [get_products, get_price, add_to_cart, recommend, checkout]