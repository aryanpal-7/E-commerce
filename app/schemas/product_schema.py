from pydantic import BaseModel
from typing import Optional
from app.models.products import ProductModel
import os


class ProductDetails(BaseModel):
    product_name: str
    price: float
    stock: int
    description: Optional[str]


class UpdateProductDetails(BaseModel):
    product_name: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    description: Optional[str]


class ProductOut(BaseModel):
    product_name: str
    price: float
    stock: int
    owner_id: int
    description: Optional[str]
    image_path: Optional[str] = None

    class Config:
        from_attributes = True
