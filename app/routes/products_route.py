from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.product_schema import ProductDetails, ProductOut
from app.core.database import get_db
from app.services.product_services import add_products, update_product, delete_product
from app.models.products import ProductModel
from app.core.security import get_current_user
from app.models.users import UserModel
from typing import List

router = APIRouter()


def check_admin(role):
    """
    Checks if the user is an admin. If not, raises a 400 HTTPException.

    Args:
        role (str): The user's role.

    Raises:
        HTTPException: If the role is not "admin".
    """

    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only Admins are allowed."
        )


def validate_fields(product_name: str, price: float, stock: int):
    """
    Validates the product details. If any of the details are invalid
    raises a 400 HTTPException.

    Args:
        product_name (str): The product name.
        price (float): The product price.
        stock (int): The product stock.

    Raises:
        HTTPException: If any of the details are invalid.
    """
    if not product_name or price <= 0 or stock <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid details or Details are missing.",
        )


@router.get("/all", response_model=List[ProductOut])
def get_all_product(
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Retrieves all products from the database.

    Args:
        limit (int): The maximum number of products to return. Defaults to 10.
        offset (int): The number of products to skip before returning. Defaults to 0.
        db (Session): The database session.

    Returns:
        List[ProductOut]: A list of products.

    """

    data = db.query(ProductModel).offset(offset).limit(limit).all()
    return data


@router.post("/add")
def add_products_info(
    product_details: ProductDetails,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Adds a new product to the database.

    This endpoint allows an admin user to add a new product to the system.
    It checks that the user is an admin and validates the product details
    before adding it.

    Args:
        product_details (ProductDetails): The details of the product to be added.
        user (UserModel): The current user retrieved from the access token.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing a success message and the product details.

    Raises:
        HTTPException: If the user is not an admin or if the product details are invalid.
    """

    check_admin(user.role)
    validate_fields(
        product_details.product_name, product_details.price, product_details.stock
    )

    return add_products(product_details, user.id, db)


@router.put("/update/{product_id}")
def update_product_info(
    product_id: int,
    product_details: ProductDetails,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Updates a product in the database.

    This endpoint allows an admin user to update the details of an existing product.
    It checks that the user is an admin and validates the product details before
    updating the product.

    Args:
        product_id (int): The id of the product to be updated.
        product_details (ProductDetails): The details of the product to be updated.
        user (UserModel): The current user retrieved from the access token.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing a success message and the updated product details.

    Raises:
        HTTPException: If the user is not an admin or if the product details are invalid.
    """

    check_admin(user.role)
    validate_fields(
        product_details.product_name, product_details.price, product_details.stock
    )

    return update_product(product_details, product_id, db)


@router.delete("/delete/{product_id}")
def delete_product_info(
    product_id: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Deletes a product from the database.

    This endpoint allows an admin user to delete an existing product by providing the product id. It checks that the user is an admin before deleting the product.

    Args:
        product_id (int): The id of the product to be deleted.
        user (UserModel): The current user retrieved from the access token.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the user is not an admin.
    """
    check_admin(user.role)
    return delete_product(product_id, user, db)
