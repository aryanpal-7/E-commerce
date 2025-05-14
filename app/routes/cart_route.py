from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cart_schema import CartDetails
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.users import UserModel
from app.models.products import ProductModel
from app.models.orders import OrderModel
from app.models.carts import CartModel
from app.routes.user_route import check_user
from app.services.cart_services import (
    validate_and_add_to_cart,
    cart_details,
    delete_cart_item_details,
    update_cart,
    cart_order_items,
)
from app.schemas.cart_schema import CartResponse, CartOut
from typing import List

router = APIRouter(prefix="/cart")


@router.post("/add/{product_id}")
def add_cart_product(
    product_id: int,
    cart: CartDetails,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    check_user(user.role)

    return validate_and_add_to_cart(user, cart.quantity, product_id, db)


@router.get("/get", response_model=CartResponse)
def get_cart_items(
    user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
):
    check_user(user.role)
    data = cart_details(user, db)
    cart_items = [
        CartOut(
            product_id=item.product_id,
            quantity=item.quantity,
            owner=item.owner.name,
            seller=item.product.admin.name,
            product_name=item.product.product_name,
            price=item.product.price,
            item_total=item.product.price * item.quantity,
        )
        for item in data
    ]
    total_price = sum(item.product.price * item.quantity for item in data)

    return CartResponse(cart_items=cart_items, cart_total_price=total_price)


@router.put("/update/{product_id}")
def update_cart_items(
    product_id: int,
    new_quantity: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_user(user.role)

    return update_cart(user, product_id, new_quantity, db)


@router.delete("/delete/{product_id}")
def delete_cart_item(
    product_id: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_user(user.role)
    return delete_cart_item_details(user, product_id, db)


@router.post("/order")
def order_cart_items(
    user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
):

    data = cart_details(user, db)
    product_ids = [item.product_id for item in data]

    return cart_order_items(product_ids, user, db)
