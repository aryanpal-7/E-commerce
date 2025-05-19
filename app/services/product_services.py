from app.models.products import ProductModel
from app.models.users import UserModel
from fastapi import HTTPException, status, UploadFile, File
from app.crud.products import add_product, update_product_info, delete_product_info
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductDetails, UpdateProductDetails
import os, uuid


def add_products(
    product_detail: ProductModel, image: UploadFile | None, id: int, db: Session
):
    """
    Adds a new product to the database.

    Args:
        product_detail (ProductModel): The product details to be added.
        image (UploadFile|None): The image file to be uploaded.
        id (int): The owner's ID.
        db (Session): The database session.

    Raises:
        HTTPException: If the product already exists with the same name under the same owner.
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
    image_path = None
    if image:
        ext = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        image_dir = os.path.join("images", "upload")

        os.makedirs(image_dir, exist_ok=True)

        image_path = os.path.join(image_dir, unique_filename)
        with open(image_path, "wb") as f:
            f.write(image.file.read())

        image_path = image_path.replace("\\", "/")
    return add_product(product_detail, image_path, id, db)


def update_product(
    product_detail: UpdateProductDetails,
    image: UploadFile | None,
    product_id: int,
    db: Session,
):
    """
    Updates a product in the database.

    Args:
        product_detail (UpdateProductDetails): The product details to be updated.
        image (UploadFile|None): The image file to be uploaded.
        product_id (int): The ID of the product to be updated.
        db (Session): The database session.

    Raises:
        HTTPException: If the product doesn't exists.
    """
    data = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product doesn't exists."
        )
    image_path = None
    if image:
        ext = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        image_dir = os.path.join("images", "upload")
        os.makedirs(image_dir, exist_ok=True)

        image_path = os.path.join(image_dir, unique_filename)
        with open(image_path, "wb") as f:
            f.write(image.file.read())

        image_path = image_path.replace("\\", "/")
    return update_product_info(product_detail, image_path, data, db)


def delete_product(id: int, user: UserModel, db: Session) -> dict[str, str]:
    """
    Deletes a product from the database.

    Args:
        id (int): The ID of the product to be deleted.
        user (UserModel): The user model object.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message.

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
