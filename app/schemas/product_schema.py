from pydantic import BaseModel


class ProductDetails(BaseModel):
    product_name: str
    price: float
    stock: int

