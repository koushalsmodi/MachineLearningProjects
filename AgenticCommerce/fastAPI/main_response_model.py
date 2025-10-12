from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class BaseUser(BaseModel):
    username : str
    email: EmailStr
    full_name: str | None = None
    
class UserIn(BaseModel):
    password: str
    
    
@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user


"""
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    

# Client -> Server
@app.post("/items/", response_model = Item)
async def create_item(item: Item) -> Any:
    return item

# Server -> Client
@app.get("/items/", response_model = list[Item])
async def read_items() -> Any:
    return [ 
            Item(name = "Portal Waterbottle", price = 42.0),
            Item(name = "Apple Macbook", price = 2000.19)
            
    ]
"""