from app.models.products import ProductModel
from app.models.carts import CartModel
from app.models.users import UserModel
from fastapi import HTTPException, status
from app.crud.cart import add_product, delete_cart_product, update_cart_details
from app.crud.order import add_ordered_cart_items
from app.schemas.cart_schema import CartOut
from typing import List
from sqlalchemy.orm import Session


def check_cart(user_id, product_id, db):
    """
    Checks if a product is already in the user's cart.

    Args:
        user_id (int): The ID of the user.
        product_id (int): The ID of the product.
        db (Session): The database session.

    Raises:
        HTTPException: If the product already exists in the cart, raises a 409 Conflict.
    """

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


def get_product_or_404(data: ProductModel):
    """
    Raises a 404 Not Found if the product is not found.

    Args:
        data (ProductModel): The product model object.

    Raises:
        HTTPException: If the product is not found, raises a 404 Not Found.
    """
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )
    return


def check_stock_availablity(stock: int, quantity: int):
    """
    Checks if the stock is available for the given quantity.

    Args:
        stock (int): The available stock.
        quantity (int): The quantity to be ordered.

    Raises:
        HTTPException: If the stock is unavailable or if the quantity is more
            than the available stock, raises a 400 Bad Request.
    """

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


def validate_and_add_to_cart(
    user: UserModel, quantity: int, product_id: int, db: Session
) -> CartModel:
    """
    Validates the product and adds it to the user's cart.

    First, it checks if the product is already in the user's cart and raises a 400
    if it is. Then, it checks if the product exists in the database and raises a 404
    if it does not. Finally, it checks if the stock is available for the given quantity
    and raises a 400 if it is not.

    Args:
        user (UserModel): The user model object.
        quantity (int): The quantity of the product to be added.
        product_id (int): The id of the product to be added.
        db (Session): The database session.

    Returns:
        CartModel: The added product's row in the cart table.

    Raises:
        HTTPException: If the product is already in the user's cart, if the product is
            not found, or if the stock is unavailable or if the quantity is more than
            the available stock.
    """

    data = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    check_cart(user.id, product_id, db)
    get_product_or_404(data)
    check_stock_availablity(data.stock, quantity)

    return add_product(user.id, quantity, product_id, db)


def cart_details(user: UserModel, db: Session) -> List[CartModel]:
    """
    Returns the user's cart items.

    Args:
        user (UserModel): The user model object.
        db (Session): The database session.

    Returns:
        List[CartModel]: The cart items.

    Raises:
        HTTPException: If the cart is empty, raises a 404 Not Found.
    """
    data = db.query(CartModel).filter(CartModel.owner_id == user.id).all()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Empty.")
    return data


def update_cart(user: UserModel, product_id: int, new_quantity: int, db: Session):
    """
    Updates the quantity of a product in the user's cart.

    This function checks if the product exists and is in the user's cart,
    then verifies the stock availability for the new quantity before updating
    the cart item.

    Args:
        user (UserModel): The user model object.
        product_id (int): The ID of the product to update.
        new_quantity (int): The new desired quantity of the product.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message and the updated cart item details.

    Raises:
        HTTPException: If the product is not found, not in the cart, or if the stock is
                       unavailable for the requested quantity.
    """

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


def delete_cart_item_details(
    user: UserModel, product_id: int, db: Session
) -> dict[str, str]:
    """
    Deletes a product from the user's cart.

    Args:
        user (UserModel): The user model object.
        product_id (int): The id of the product to be deleted.
        db (Session): The database session.

    Returns:
        dict[str, str]: A dictionary containing a success message.

    Raises:
        HTTPException: If the cart item does not exist, raises a 404 Not Found.
    """

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


def cart_order_items(product_ids: List, user: UserModel, db: Session):
    """
    Places an order for all products in the given list of product IDs currently in the user's cart.

    Args:
        product_ids (List): A list of product IDs to place an order for.
        user (UserModel): The user model object.
        db (Session): The database session.

    Returns:
        dict: A dictionary with order details and a list of unavailable products.
    """
    fetched_products = (
        db.query(ProductModel).filter(ProductModel.id.in_(product_ids)).all()
    )
    stock_available = [p for p in fetched_products if p.stock > 0]
    stock_unavailable = [p for p in fetched_products if p.stock <= 0]

    existing_ids = {p.id for p in fetched_products}
    missing_products = set(product_ids) - existing_ids
    return add_ordered_cart_items(
        stock_available=stock_available,
        stock_unavailable=stock_unavailable,
        user=user,
        db=db,
    )
