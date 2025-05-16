from app.models.products import ProductModel
from app.models.users import UserModel
from fastapi import HTTPException, status
from app.crud.products import add_product, update_product_info, delete_product_info
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductDetails


def add_products(product_detail: ProductModel, id: int, db: Session):
    """
    Adds a new product to the database.

    Args:
        product_detail (ProductModel): The product details to be added.
        id (int): The owner's ID.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message and the product details.

    Raises:
        HTTPException: If an error occurs while adding the product, an HTTPException
                       with a 409 status code is raised, indicating a conflict with an existing product.
    """
    data = (
        db.query(ProductModel)
        .filter(
            ProductModel.product_name == product_detail.product_name,
            ProductModel.owner_id == id,
        )
        .first()
    )
    if data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product Already Exists with this name.",
        )
    return add_product(product_detail, id, db)


def update_product(product_detail: ProductDetails, product_id: int, db: Session):
    """
    Updates an existing product's details in the database.

    Args:
        product_detail (ProductDetails): The new product details to update.
        product_id (int): The ID of the product to be updated.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message and the updated product details.

    Raises:
        HTTPException: If the product is not found, raises a 404 Not Found.
    """

    data = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product doesn't exists."
        )

    return update_product_info(product_detail, data, db)


def delete_product(id: int, user: UserModel, db: Session) -> dict[str, str]:
    """
    Deletes a product from the database.

    Args:
        id (int): The ID of the product to be deleted.
        user (UserModel): The user model object associated with the product.
        db (Session): The database session.

    Returns:
        dict[str, str]: A dictionary containing a success message.

    Raises:
        HTTPException: If the product is not found, raises a 404 Not Found.
    """

    data = (
        db.query(ProductModel)
        .filter(ProductModel.id == id, ProductModel.owner_id == user.id)
        .first()
    )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )
    return delete_product_info(data, db)
