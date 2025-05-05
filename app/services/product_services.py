from app.models.products import ProductModel
from fastapi import HTTPException, status
from app.crud.products import add_product, update_product_info, delete_product_info


def add_products(product_detail, id, db):
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


def update_product(product_detail, product_id, db):
    data = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product doesn't exists."
        )

    return update_product_info(product_detail, data, db)


def delete_product(id: int, user, db):
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
