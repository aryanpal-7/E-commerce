from app.models.products import ProductModel
from app.models.carts import CartModel
from fastapi import HTTPException, status
from app.crud.cart import add_product, delete_cart_product, update_cart_details
from app.schemas.cart_schema import CartOut
from typing import List


def check_cart(user_id, product_id, db):
    data = (
        db.query(CartModel)
        .filter(CartModel.owner_id == user_id, CartModel.product_id == product_id)
        .first()
    )

    if data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product already Exists in the cart.",
        )
    return


def get_product_or_404(data):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )
    return


def check_stock_availablity(stock, quantity):
    if stock <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Stock unavailable."
        )
    if quantity > stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Available stock is only {stock}.You cannot order more than this.",
        )
    return


def validate_and_add_to_cart(user, quantity, product_id, db):
    data = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    check_cart(user.id, product_id, db)
    get_product_or_404(data)
    check_stock_availablity(data.stock, quantity)

    return add_product(user.id, quantity, product_id, db)


def cart_details(user, db):
    data = db.query(CartModel).filter(CartModel.owner_id == user.id).all()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Empty.")
    return data


def update_cart(user, product_id, new_quantity, db):
    data = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    get_product_or_404(data)
    cart_data = (
        db.query(CartModel)
        .filter(CartModel.product_id == product_id, CartModel.owner_id == user.id)
        .first()
    )
    if not cart_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product is not in the cart."
        )
    check_stock_availablity(data.stock, new_quantity)
    return update_cart_details(cart_data, new_quantity, db)


def delete_cart_item_details(user, product_id, db):
    data = (
        db.query(CartModel)
        .filter(CartModel.product_id == product_id, CartModel.owner_id == user.id)
        .first()
    )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart item doesn't exists."
        )

    return delete_cart_product(data, db)
