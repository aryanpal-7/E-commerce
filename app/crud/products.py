from app.models.products import ProductModel
from fastapi import HTTPException, status
from app.schemas.product_schema import UpdateProductDetails
from sqlalchemy.orm import Session
import os


def add_product(product_detail: ProductModel, image_path, id: int, db: Session):
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
                       with a 500 status code is raised, indicating an internal server error.
    """

    try:

        data = ProductModel(
            product_name=product_detail.product_name,
            stock=product_detail.stock,
            price=product_detail.price,
            owner_id=id,
            image_path=image_path,
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return {"message": "Product added successfully", "Product Details": data}
    except Exception as e:
        db.rollback()
        if os.path.exists(image_path):
            os.remove(image_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error.{e}",
        )


def update_product_info(
    product_detail: UpdateProductDetails,
    image_path: str | None,
    data: ProductModel,
    db: Session,
):
    """
    Updates a product in the database.

    Args:
        product_detail (UpdateProductDetails): The product details to be updated.
        image_path (str|None): The path of the new image file, if any.
        data (ProductModel): The existing product model to be updated.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message and the updated product details.

    Raises:
        HTTPException: If an error occurs while updating the product, an HTTPException
                       with a 500 status code is raised, indicating an internal server error.
    """

    old_image_path = None
    if product_detail.product_name:
        data.product_name = product_detail.product_name
    if product_detail.price is not None and product_detail.price >= 0:
        data.price = product_detail.price
    if product_detail.stock is not None and product_detail.stock >= 0:
        data.stock = product_detail.stock
    if image_path:
        old_image_path = (
            data.image_path.replace("/", os.sep) if data.image_path else None
        )
        data.image_path = image_path
    try:
        db.commit()
        db.refresh(data)
        if old_image_path and os.path.exists(old_image_path):
            try:
                os.remove(old_image_path)
            except Exception as e:
                print("Cannot delete image.")
    except Exception:
        db.rollback()
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error Occured.",
        )
    return {"message": "Product details updated successfully", "data": data}


def delete_product_info(product_detail: ProductModel, db: Session) -> dict[str, str]:
    """
    Deletes a product from the database.

    Args:
        product_detail (ProductModel): The product details to be deleted.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If an error occurs while deleting the product, an HTTPException
                       with a 500 status code is raised, indicating an internal server error.
    """

    try:
        image_path = (
            product_detail.image_path.replace("/", os.sep)
            if product_detail.image_path
            else None
        )
        db.delete(product_detail)
        db.commit()
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print("Cannot delete image.")
        return {"message": "product deleted Successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
