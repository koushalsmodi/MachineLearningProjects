from fastapi import FastAPI
from pydantic import BaseModel

# Request, POST is client -> server

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
app = FastAPI()

@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    
    result =  {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


    # item_dict = item.dict()
    # if item.tax is not None:
    #     price_with_tax = item.price + item.tax 
    #     item_dict.update({"price_with_tax": price_with_tax})
    # return item_dict