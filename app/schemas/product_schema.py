from pydantic import BaseModel
from typing import Optional
from app.models.products import ProductModel
import os
class ProductDetails(BaseModel):
    product_name: str
    price: float
    stock: int
    # product_image: Optional[str] = None
     
    # class Config:
    #     json_schema_extra = {
    #         "example": {"product_name": "Iphone", "price": 999.9, "stock": 100,"product_image":"image.jpg"}
    #     }


class ProductOut(BaseModel):
    product_name: str
    price: float
    stock: int
    owner_id: int
    image_path: Optional[str] = None
    
    class Config:
        from_attributes = True

    