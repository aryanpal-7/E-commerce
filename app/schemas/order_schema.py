from pydantic import BaseModel


class OrderDetails(BaseModel):
    quantity: int


class OrderOutput(BaseModel):

    product_name: str
    price: float
    quantity: int
    seller_name: str

    class Config:
        from_attributes = True
