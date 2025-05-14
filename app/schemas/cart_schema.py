from pydantic import BaseModel
from typing import List


class CartDetails(BaseModel):
    # product_id: int
    quantity: int
    # owner_id: int


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
