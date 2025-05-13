from app.models.products import ProductModel
from fastapi import HTTPException, status
from app.schemas.product_schema import ProductDetails


def add_product(product_detail, id, db):
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


def update_product_info(product_detail: ProductDetails, data, db):

    if product_detail.product_name:
        data.product_name = product_detail.product_name
    if product_detail.price >= 0:
        data.price = product_detail.price

    if product_detail.stock >= 0:
        data.stock = product_detail.stock
    db.commit()
    db.refresh(data)
    return {"message": "Product details updated successfully", "data": data}


def delete_product_info(product_detail, db):
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
