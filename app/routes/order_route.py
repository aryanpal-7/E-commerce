from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.users import UserModel
from app.models.orders import OrderModel
from app.services.order_services import check_order_details, delete_order_details
from app.schemas.order_schema import OrderDetails, OrderOutput

router = APIRouter()


@router.post("/order/{product_id}")
def order_product(
    product_id: int,
    order: OrderDetails,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return check_order_details(product_id, order.quantity, user, db)


@router.get("/order")
def get_all_order(
    user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
):
    return db.query(OrderModel).filter(OrderModel.owner_id == user.id).all()


@router.delete("/order/cancel/{order_id}")
def delete_order(
    order_id: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_order_details(order_id, user, db)
