from fastapi import FastAPI
from models import ProductIn, ProductOut, CartItemIn, CartItemOut, Order, CheckoutIn
from fastapi import HTTPException
from datetime import datetime
import logging
import random

# time of log event, severity (eg: INFO, WARNING), message
logging.basicConfig(level = logging.INFO, 
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    filename = 'mini_shop.log',
                    filemode='a')


products = []
next_available_id = 1
cart = []
orders = []
next_order_id = 1

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Mini Shop API"}


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
async def create_cart_item(cart_item_in: CartItemIn):
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

def simulate_payment(probability_for_true):
    return random.random() < probability_for_true


# POST: Client -> Server 
# Purpose: convert cart to order
@app.post("/checkout", response_model=Order)
async def create_order(checkoutin: CheckoutIn):
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
async def read_order():
    logging.debug(f"Orders list requested - {len(orders)} orders total")
    return orders