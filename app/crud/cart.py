from app.models.carts import CartModel
from sqlalchemy.orm import Session


def add_product(user_id: int, quantity: int, product_id: int, db: Session) -> CartModel:
    """
    Adds a product to the user's cart

    Args:
        user_id (int): The user's id
        quantity (int): The quantity of the product to be added
        product_id (int): The product's id
        db (Session): The database connection

    Returns:
        CartModel: The added product's row in the cart table
    """
    data = CartModel(product_id=product_id, quantity=quantity, owner_id=user_id)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def update_cart_details(data: CartModel, quantity: int, db: Session) -> dict:
    """
    Updates the quantity of a product in the user's cart

    Args:
        data (CartModel): The row to be updated in the cart table
        quantity (int): The new quantity of the product
        db (Session): The database connection

    Returns:
        dict: A dictionary containing a success message and the updated data
    """
    data.quantity = quantity
    db.commit()
    db.refresh(data)
    return {"message": "Updated successfully", "data": data}


def delete_cart_product(data: CartModel, db: Session) -> dict[str, str]:
    """
    Deletes a product from the user's cart

    Args:
        data (CartModel): The row to be deleted in the cart table
        db (Session): The database connection

    Returns:
        dict[str, str]: A dictionary containing a success message
    """

    db.delete(data)
    db.commit()

    return {"message": "Data Deleted Successfully."}
