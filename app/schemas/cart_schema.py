from pydantic import BaseModel
from typing import List


class CartDetails(BaseModel):
    quantity: int

    class Config:
        json_schema_extra = {"example": {"quantity": 10}}


class CartOut(BaseModel):
    seller: str
    product_name: str
    product_id: int
    owner: str
    quantity: int
    price: float
    item_total: float


class CartResponse(BaseModel):
    cart_items: List[CartOut]
    cart_total_price: float
