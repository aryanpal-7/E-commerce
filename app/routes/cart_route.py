from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cart_schema import CartDetails
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.users import UserModel
from app.routes.user_route import check_user
from app.services.cart_services import (
    validate_and_add_to_cart,
    cart_details,
    delete_cart_item_details,
    update_cart,
)
from app.schemas.cart_schema import CartOut
from typing import List

router = APIRouter()


@router.post("/addproducttocart/{product_id}")
def add_cart_product(
    product_id: int,
    cart: CartDetails,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    check_user(user.role)

    return validate_and_add_to_cart(user, cart.quantity, product_id, db)


@router.get("/getcartitems", response_model=List[CartOut])
def get_cart_items(
    user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
):
    check_user(user.role)
    data = cart_details(user, db)
    return [
        CartOut(
            product_id=item.product_id,
            stock=item.quantity,
            owner=item.owner.name,
            Seller=item.product.admin.name,
            product_name=item.product.product_name,
        )
        for item in data
    ]


@router.put("/updatecart/{product_id}")
def update_cart_items(
    product_id: int,
    new_quantity: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_user(user.role)

    return update_cart(user, product_id, new_quantity, db)


@router.delete("/cart/{product_id}")
def delete_cart_item(
    product_id: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_user(user.role)
    return delete_cart_item_details(user, product_id, db)
