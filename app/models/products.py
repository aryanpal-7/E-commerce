from sqlalchemy import Column, Integer, String, ForeignKey, FLOAT
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    product_name = Column(String, unique=True, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(FLOAT, nullable=False)

    cart = relationship("CartModel", back_populates="product")
