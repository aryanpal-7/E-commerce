from app.models.orders import OrderModel
from app.models.products import ProductModel
from fastapi import HTTPException, status
from app.crud.order import add_order, delete_order


def check_if_product_available(data, quantity):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )
    if data.stock < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Current Stock is {data.stock}",
        )
    return


def validate_order_exists(data):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order Not found."
        )
    return


def check_order_details(product_id: int, quantity, user, db):
    product_data = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    check_if_product_available(product_data, quantity)
    return add_order(
        product_data=product_data, user_data=user, quantity=quantity, db=db
    )


def delete_order_details(order_id: int, user, db):
    data = (
        db.query(OrderModel)
        .filter(OrderModel.id == order_id, OrderModel.owner_id == user.id)
        .first()
    )
    validate_order_exists(data)
    return delete_order(data, db)
