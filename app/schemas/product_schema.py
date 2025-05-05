from pydantic import BaseModel


class ProductDetails(BaseModel):
    product_name: str
    price: float
    stock: int

class ProductOut(BaseModel):
    product_name: str
    price: float
    stock: int
    owner_id:int
    
    class Config:
        from_attributes=True