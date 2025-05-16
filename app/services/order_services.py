from app.models.orders import OrderModel
from app.models.products import ProductModel
from fastapi import HTTPException, status
from app.crud.order import add_order, delete_order
from app.models.users import UserModel
from sqlalchemy.orm import Session


def check_if_product_available(data, quantity) -> None:
    """
    Checks if the product is available with the required quantity.

    Args:
        data (ProductModel): The product data object.
        quantity (int): The required quantity of the product.

    Raises:
        HTTPException: If the product is not found or if the stock is less than the required quantity.
    """

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


def validate_order_exists(data: OrderModel) -> None:
    """
    Validates if the order exists.

    Args:
        data (OrderModel): The order object

    Raises:
        HTTPException: If the order is not found.
    """
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order Not found."
        )
    return


def check_order_details(
    product_id: int, quantity: int, user: UserModel, db: Session
) -> dict[str, str]:
    """
    Places an order for a product.

    Args:
        product_id (int): The id of the product to be ordered.
        quantity (int): The quantity of the product being ordered.
        user (UserModel): The user model object.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary with the order details, including the order ID, product name, price, quantity, seller name, status, and total price.
    """

    product_data = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    check_if_product_available(product_data, quantity)
    return add_order(
        product_data=product_data, user_data=user, quantity=quantity, db=db
    )


def delete_order_details(order_id: int, user: UserModel, db: Session) -> dict[str, str]:
    """
    Cancels an order based on the order ID.

    Args:
        order_id (int): The id of the order to be cancelled.
        user (UserModel): The user model object.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary with a success message.
    """
    data = (
        db.query(OrderModel)
        .filter(OrderModel.id == order_id, OrderModel.owner_id == user.id)
        .first()
    )
    validate_order_exists(data)
    return delete_order(data, db)
