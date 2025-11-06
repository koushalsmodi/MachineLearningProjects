from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
    
class ProductIn(BaseModel):
    name: str 
    description : str 
    price: float 
    currency: str 
    inventory: int 
    category: str 
    
class ProductOut(BaseModel):
    id: int
    name: str 
    description : str 
    price: float 
    currency: str 
    inventory: int 
    category: str 
    
class CartItemIn(BaseModel):
    product_id: int 
    quantity: int = 1

class CartItemOut(BaseModel):
    
    product_id: int
    name: str 
    price: float 
    currency: str
    quantity: int 
    subtotal: float

class CheckoutIn(BaseModel):
    
    customer_name: str 
    email: EmailStr
    
class Order(BaseModel):
    order_id: int
    customer_name: str
    email: EmailStr 
    items : List[CartItemOut]
    shipping_price: float = 0.0
    tax_price: float = 0.0
    total_price: float 
    paid: bool = False # set True on successful checkout
    status: str = "pending" # pending, paid, shipped, etc.
    created_at : datetime

    
    
    