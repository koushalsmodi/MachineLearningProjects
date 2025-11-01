from fastapi import FastAPI
from models import ProductIn, ProductOut, CartItemIn, CartItemOut, Order, CheckoutIn
from fastapi import HTTPException
from datetime import datetime
import logging
# time of log event, severity (eg: INFO, WARNING), message
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')


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
    logging.info("Product {id} created: {name}, price {price} {currency}")
    
    return result

# Get: Server -> Client
@app.get("/products", response_model = list[ProductOut])
async def read_products():
    logging.debug("Product list requested - {len(products)} items")
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
            logging.info("Added Product {product_id} * {quantity} to cart (subtotal {subtotal}).")
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
    logging.info("Cart viewed - {len(cart)} items, total {total}")
        
    return display_cart_summary

# POST: Client -> Server 
# Purpose: convert cart to order
@app.post("/checkout", response_model=Order)
async def create_order(checkoutin: CheckoutIn):
    logging.info("Checkout initiated by {checkoutin.email}")
    global next_order_id
    if not cart:
        raise HTTPException(status_code=400, detail="No items in the cart for ordering")

    total = sum(item.subtotal for item in cart)
    shipping = 10.0
    tax = total * 0.10
    grand_total = total + shipping + tax

    order_obj = Order(
        order_id=next_order_id,
        customer_name=checkoutin.customer_name,
        email=checkoutin.email,
        items=cart.copy(),
        shipping_price=shipping,
        tax_price=tax,
        total_price=grand_total,
        paid=True,
        status="paid",
        created_at=datetime.now()
    )

    orders.append(order_obj)
    logging.info("Order {order_id} completed successfully - total {grand_total}")
    next_order_id += 1
    cart.clear()  

    return order_obj
# Get: Server -> Client
# Purpose: list all completed orders
@app.get("/orders", response_model=list[Order])
async def read_order():
    logging.debug("Orders list requested - {len(orders)} orders total")
    return orders