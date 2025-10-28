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
    
    
    
    
   
    
    
    
    
    