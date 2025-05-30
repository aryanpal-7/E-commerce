from pydantic import BaseModel


class OrderDetails(BaseModel):
    quantity: int

    class Config:
        json_schema_extra = {"example": {"quantity": 10}}


class OrderOutput(BaseModel):
    order_id: int
    product_name: str
    price: float
    quantity: int
    seller_name: str
    status: str
    total_price: float

    class Config:
        from_attributes = True
