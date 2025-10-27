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
    
def test_read_product():
    
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
@app.post("/products", response_model = ProductOut)
def test_create_cart_item():
    
    cart_data = {
        "product_id": 10,
        "quantity": 2000
    }
    
    response = client.post("/cart/add", json = cart_data)
    assert response.status_code == 200 
    data = response.json()
    assert data["product_id"] == cart_data["product_id"]
    