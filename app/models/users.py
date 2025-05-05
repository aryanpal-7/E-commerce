from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role=Column(String, nullable=False, default="user")
    
    admin_id=relationship("ProductModel", back_populates="admin")
    cart = relationship("CartModel", back_populates="owner")
