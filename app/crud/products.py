from app.models.products import ProductModel
from fastapi import HTTPException, status
from app.schemas.product_schema import ProductDetails
from sqlalchemy.orm import Session


def add_product(product_detail: ProductModel, id: int, db: Session):
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
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return {"message": "Product added successfully", "Product Details": data}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error.{e}",
        )


def update_product_info(
    product_detail: ProductDetails, data: ProductModel, db: Session
):
    """
    Updates the product details in the database.

    Args:
        product_detail (ProductDetails): The product details to be updated.
        data (ProductModel): The product details that will be updated with new product details.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message and the updated product details.
    """

    if product_detail.product_name:
        data.product_name = product_detail.product_name
    if product_detail.price >= 0:
        data.price = product_detail.price

    if product_detail.stock >= 0:
        data.stock = product_detail.stock
    db.commit()
    db.refresh(data)
    return {"message": "Product details updated successfully", "data": data}


def delete_product_info(product_detail: ProductModel, db: Session) -> dict[str, str]:
    """
    Deletes a product from the database.

    Args:
        product_detail (ProductModel): The product model object to be deleted.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message.
    """

    try:
        db.delete(product_detail)
        db.commit()
        return {"message": "product deleted Successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
