import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

products_to_add = [
    {
        "name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse with USB receiver",
        "price": 25.99,
        "currency": "USD",
        "inventory": 50,
        "category": "Electronics"
    },
    {
        "name": "USB-C Cable",
        "description": "6ft braided USB-C charging cable",
        "price": 12.99,
        "currency": "USD",
        "inventory": 100,
        "category": "Electronics"
    },
    {
        "name": "Notebook Set",
        "description": "Pack of 3 lined notebooks",
        "price": 15.99,
        "currency": "USD",
        "inventory": 75,
        "category": "Office Supplies"
    },
    {
        "name": "Water Bottle",
        "description": "32oz stainless steel insulated water bottle",
        "price": 29.99,
        "currency": "USD",
        "inventory": 40,
        "category": "Home & Kitchen"
    },
    {
        "name": "Phone Stand",
        "description": "Adjustable aluminum phone stand",
        "price": 18.99,
        "currency": "USD",
        "inventory": 60,
        "category": "Electronics"
    }
]

for product in products_to_add:
    response = requests.post(
        "http://127.0.0.1:8000/products",
        json=product
    )
    if response.status_code == 200:
        print(f"✓ Added: {product['name']} - ${product['price']}")
    else:
        print(f"✗ Failed to add: {product['name']}")

print("\nAll products added! Testing get products:")
response = requests.get("http://127.0.0.1:8000/products")
print(f"Total products in store: {len(response.json())}")