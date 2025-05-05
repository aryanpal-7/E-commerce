from sqlalchemy import Column, Integer, String, ForeignKey, FLOAT
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(FLOAT, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    admin = relationship("UserModel", back_populates="admin_id")
    cart = relationship("CartModel", back_populates="product")
