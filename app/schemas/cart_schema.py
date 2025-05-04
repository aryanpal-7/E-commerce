from pydantic import BaseModel


class CartDetails(BaseModel):
    product_id: int
    quantity: int
    owner_id: int

    class Config:
        from_attributes = True
