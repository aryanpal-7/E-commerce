from pydantic import BaseModel


class ProductDetails(BaseModel):
    product_name: str
    price: float
    stock: int

    class Config:
        json_schema_extra = {
            "example": {"product_name": "Iphone", "price": 999.9, "stock": 100}
        }


class ProductOut(BaseModel):
    product_name: str
    price: float
    stock: int
    owner_id: int

    class Config:
        from_attributes = True
