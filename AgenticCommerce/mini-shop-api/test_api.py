from main import app
from fastapi.testclient import TestClient
from models import ProductIn, ProductOut, CartItemIn, CartItemOut, Order, CheckoutIn


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Mini Shop API"}
    
def test_create_product():
    product_data = {
        "name": "Apple",
        "description": "macbook",
        "price": 42.00,
        "currency": "USD",
        "inventory": 2000,
        "category": "Electronics"
    }
    
    response = client.post("/products", json = product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert "id" in data
    return data
    
def test_read_products():
    
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
def test_create_cart_item():
    product_data = {
        "name": "Apple",
        "description": "macbook",
        "price": 42.00,
        "currency": "USD",
        "inventory": 2000,
        "category": "Electronics"
    }
    products_response = client.post("/products", json = product_data)
    assert products_response.status_code == 200 
    
    product_json = products_response.json()
    product_id = product_json["id"]
    
    cart_data = {
        "product_id": product_id,
        "quantity": 2
    }
    
    cart_response = client.post("/cart/add", json = cart_data)
    assert cart_response.status_code == 200 

    
    data = cart_response.json()
    
    assert data["product_id"] == product_id
    assert data["name"] == product_json["name"]
    assert data["price"] == product_json["price"]
    assert data["currency"] == product_json["currency"]
    assert data["quantity"] == cart_data["quantity"]
    assert data["subtotal"] == data["price"] * data["quantity"]
    
def test_read_cart():
    
    product_data = {
        "name": "Apple",
        "description": "macbook",
        "price": 42.00,
        "currency": "USD",
        "inventory": 2000,
        "category": "Electronics"
    }
    products_response = client.post("/products", json = product_data)
    assert products_response.status_code == 200 
    
    product_json = products_response.json()
    product_id = product_json["id"]
    
    cart_data = {
        "product_id": product_id,
        "quantity": 2
    }
    
    cart_response = client.post("/cart/add", json = cart_data)
    assert cart_response.status_code == 200 
    
    response = client.get("/cart")
    assert response.status_code == 200
    
    cart_json = response.json()
    assert isinstance(cart_json, dict)
    assert "items" in cart_json
    assert isinstance(cart_json["items"], list)
    assert len(cart_json["items"]) > 0
    
# checkout -> post/checkout test_checkout
def test_create_checkout():
    
    product_data = {
        "name": "Apple",
        "description": "macbook",
        "price": 42.00,
        "currency": "USD",
        "inventory": 2000,
        "category": "Electronics"
    }
    products_response = client.post("/products", json = product_data)
    assert products_response.status_code == 200 
    
    product_json = products_response.json()
    product_id = product_json["id"]
    
    
    cart_data = {
        "product_id": product_id,
        "quantity": 2
    }
    
    cart_response = client.post("/cart/add", json = cart_data)
    assert cart_response.status_code == 200 
    
    checkout_data = {
    "customer_name": "John Doe",
    "email": "john@example.com"
    }
    
    checkout_response = client.post("/checkout", json = checkout_data)
    assert checkout_response.status_code == 200 
    
    checkout_json = checkout_response.json()
    
    assert checkout_json["customer_name"] == checkout_data["customer_name"]
    assert checkout_json["email"] == checkout_data["email"]
    
    assert isinstance(checkout_json, dict) 
    assert "order_id" in checkout_json
    assert "items" in checkout_json
    
    assert checkout_json["paid"] is True 
    assert checkout_json["status"] == "paid"
    
    assert isinstance(checkout_json["items"], list)
    assert len(checkout_json["items"]) > 0
    
    subtotal = sum(item["subtotal"] for item in checkout_json["items"])
    expected_total = subtotal + checkout_json["shipping_price"] + checkout_json["tax_price"]
    assert checkout_json["total_price"] == expected_total
    
    response = client.get("/cart")
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 0.0

# orders -> get/orders test_read_orders

def test_read_orders():
    
    product_data = {
        "name": "Apple",
        "description": "macbook",
        "price": 42.00,
        "currency": "USD",
        "inventory": 2000,
        "category": "Electronics"
    }
    products_response = client.post("/products", json = product_data)
    assert products_response.status_code == 200 
    
    product_json = products_response.json()
    product_id = product_json["id"]
    
    
    cart_data = {
        "product_id": product_id,
        "quantity": 2
    }
    
    cart_response = client.post("/cart/add", json = cart_data)
    assert cart_response.status_code == 200 

    checkout_data = {
    "customer_name": "John Doe",
    "email": "john@example.com"
    }
    
    checkout_response = client.post("/checkout", json = checkout_data)
    assert checkout_response.status_code == 200 
    
    checkout_json = checkout_response.json()
    
    response = client.get("/orders")
    assert response.status_code == 200
    
    orders_json = response.json()
    assert isinstance(orders_json, list)
    assert len(orders_json) > 0
    
    order = orders_json[-1]
    assert "order_id" in order 
    assert order["customer_name"] == "John Doe"
    assert order["email"] == "john@example.com" 
    assert order["paid"] is True 
    assert order["status"] == "paid"
    assert isinstance(order["items"], list)
    assert order["total_price"] > 0