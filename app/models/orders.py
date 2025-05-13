from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    event,
    Enum as SqlEnum,
)
from enum import Enum
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.products import ProductModel


class OrderStatus(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    seller_name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.PENDING)

    ownerorder = relationship("UserModel", back_populates="order")
    product = relationship("ProductModel", back_populates="orderproduct")


@event.listens_for(OrderModel, "before_delete")
def restore_stock_before_delete(mapper, connection, target):
    """BEFORE DELETE EVENT"""
    session = Session(bind=connection)
    product = (
        session.query(ProductModel).filter(ProductModel.id == target.product_id).first()
    )
    if product:
        product.stock += target.quantity
        session.flush()


@event.listens_for(OrderModel, "before_insert")
def update_stock_before_insert(mapper, connection, target):
    """BEFORE INSERT EVENT"""
    session = Session(bind=connection)
    product = (
        session.query(ProductModel).filter(ProductModel.id == target.product_id).first()
    )

    if product:

        product.stock -= target.quantity
        session.flush()
