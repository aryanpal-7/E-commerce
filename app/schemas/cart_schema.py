from pydantic import BaseModel


class CartDetails(BaseModel):
    # product_id: int
    quantity: int
    # owner_id: int


class CartOut(BaseModel):
    Seller: str
    product_name: str
    product_id: int
    owner: str
    stock: int
