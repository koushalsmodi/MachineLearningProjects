from fastapi import FastAPI

app = FastAPI()

# optional, default, required
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, prod : str, price : int = 100, description : str | None = None):
    item = {"item_id": item_id, "prod": prod, "price": price, "description": description}
    return item


# /items/SGG_ELECTRONICS?prod=apple_macbook&price=200&description=best design
# /items/SGG_ELECTRONICS?prod=apple_macbook
# /items/SGG_ELECTRONICS?prod=apple_macbook&description=best design
# /items/SGG_ELECTRONICS?prod=apple_macbook&price=200
"""
# Required query parameters
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

# Multiple Path and Query Parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item



/users/123/items/SDD_electronics

/users/123/items/SDD_electronics?q=apple

/users/123/items/SDD_electronics?q=apple&short=0

/users/123/items/SDD_electronics?q=apple&short=1



fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, type: str | None = None):
    if q and type:
        return {"item_id": item_id, "q": q, "type": type}
    return {"item_id": item_id}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short : bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
        
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
        
    return item
    
"""