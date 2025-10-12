from fastapi import FastAPI
from models import ProductIn, ProductOut

products = []
next_available_id = 1

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
    
    
    return result

# GET: Server -> Client
@app.get("/products", response_model = list[ProductOut])
async def read_products():
    return products
    