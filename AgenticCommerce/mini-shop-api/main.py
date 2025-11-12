import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from langchain.chat_models import init_chat_model
import os 

import logging
import random
from datetime import datetime
from fastapi import FastAPI, Depends, Header
from models import ProductIn, ProductOut, CartItemIn, CartItemOut, Order, CheckoutIn
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
VALID_API_KEY = os.getenv("API_KEY")

# time of log event, severity (eg: INFO, WARNING), message
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mini_shop.log", mode='w'),
        logging.StreamHandler()
    ]
)

products = []
next_available_id = 1
cart = []
orders = []
next_order_id = 1

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code = 401, detail = "Unauthorized")
    return True

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Mini Shop API"}

print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])


# POST: Client -> Server
# Add this model at the top with your other models
from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    query: str

# Then update the endpoint:
@app.post("/recommend")
async def create_recommendation_request(request: RecommendationRequest):
    query = request.query
    # products is a list available as a global variable
    prompt = f"""You are a product recommender and your role is to \n
    take user's query: {query} and advice the user with a small list or with just 1 item \n
    based on the user's budget and preferences \n
    from the catalog: {products} based on the user query. \n
    The user will be the buyer so it is of utmost importance to provide a correct response \n
    so as to have our sale successful. \n
    Output should be short and human-readable. \n
    """

    model = init_chat_model(
        "claude-sonnet-4-5-20250929",
        temperature = 0.7,
        timeout=  30,
        max_tokens = 1000,
    )

    try:
        response = model.invoke(prompt)
        print(f"\n--- {query} ({response.text}) ---")
        print(response.text.strip() if response.text else "No response returned.")
    except Exception as e:
        print(f"Error processing {query}: {e}")
        
    json_output = {
        "message": "Here's the product Anthropic recommends",
        "recommendation": response.text
    }
    
    logging.info(f"Query {query}, Recommendation: {response.text}")
    return json_output

# POST: Client -> Server
@app.post("/products", response_model = ProductOut)
async def create_product(product_in: ProductIn):
    global next_available_id
    
    result = {**product_in.dict()}
    result.update({"id": next_available_id})
    
    products.append(result)
    next_available_id += 1
    logging.info(f"Product {result['id']} created: {result['name']}, price {result['price']} {result['currency']}")
    
    return result

# Get: Server -> Client
@app.get("/products", response_model = list[ProductOut])
async def read_products():
    logging.debug(f"Product list requested - {len(products)} items")
    return products 

# POST: Client -> Server
# Purpose: add an item to the cart
@app.post("/cart/add", response_model = CartItemOut)
async def create_cart_item(cart_item_in: CartItemIn, token_check: bool = Depends(verify_token)):
    
    for product in products:
        if product["id"] == cart_item_in.product_id:
            name = product["name"]
            price = product["price"]
            currency = product["currency"]
            quantity = cart_item_in.quantity 
            subtotal = price * quantity
            
            cart_item_out = CartItemOut(
            
            product_id = product["id"],
            name = name,
            price = price,
            currency = currency,
            quantity = quantity,
            subtotal = subtotal
            )
            cart.append(cart_item_out)
            logging.info(f"Added Product {product['id']} x {quantity} to cart (subtotal {subtotal}).")
            return cart_item_out

    raise HTTPException(status_code = 404, detail = "Product not found")

# Get: Server -> Client
# Purpose: shows everything in cart
@app.get("/cart")
async def read_cart():
    if not cart:
        return {"items": [], "total": 0.0}
    
    total = 0.0
    for item in cart:
        total += item.subtotal 
    
    display_cart_summary = {
        "items": cart,
        "total": total
    }
    logging.info(f"Cart viewed - {len(cart)} items, total {total}")
        
    return display_cart_summary

def simulate_payment(probability_for_true: float) -> bool:
    return random.random() < probability_for_true


# POST: Client -> Server 
# Purpose: convert cart to order
@app.post("/checkout", response_model=Order)
async def create_order(checkoutin: CheckoutIn,  token_check: bool = Depends(verify_token)):
    logging.info(f"Checkout initiated by {checkoutin.email}")
    global next_order_id
    if not cart:
        raise HTTPException(status_code=400, detail="No items in the cart for ordering")

    total = sum(item.subtotal for item in cart)
    shipping = 10.0
    tax = total * 0.10
    grand_total = total + shipping + tax
    paid = False
    for attempt in range(3):
        result = simulate_payment(0.8)
        if result:
            logging.info(f"Payment simulation succeeded in attempt {attempt+1}")
            paid = True
            status = "paid"
            break
        
        else:
            logging.info(f"Payment simulation failed in attempt {attempt+1}")
            status = "failed"
    if not paid:
        logging.error("Payment failed after 3 retries")
        status = "failed"
        raise HTTPException(500, "Payment failed after 3 retries.")

        
    order_obj = Order(
        order_id=next_order_id,
        customer_name=checkoutin.customer_name,
        email=checkoutin.email,
        items=cart.copy(),
        shipping_price=shipping,
        tax_price=tax,
        total_price=grand_total,
        paid=paid,
        status=status,
        created_at=datetime.now()
    )

    orders.append(order_obj)
    logging.info(f"Order {order_obj.order_id} finalized with status {status} - total {grand_total}")
    next_order_id += 1
    cart.clear()  

    return order_obj
# Get: Server -> Client
# Purpose: list all completed orders

@app.get("/orders", response_model=list[Order])
async def read_order(token_check: bool = Depends(verify_token)):
    logging.debug(f"Orders list requested - {len(orders)} orders total")
    return orders