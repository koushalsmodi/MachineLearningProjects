from pydantic import BaseModel



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