from app.models.products import ProductModel
from fastapi import HTTPException, status
def add_product(product_detail,db):
    try:
        data=ProductModel(product_name=product_detail.product_name,stock=product_detail.stock,price=product_detail.price)
        db.add(data)
        db.commit()
        db.refresh(data)
        return {"message":"Product added successfully", "Product Details":data}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error.")

def update_product_info(product_detail,data,db):
    if product_detail.product_name:
        data.product_name=product_detail.product_name
    if product_detail.price:
        data.price=product_detail.price
    if product_detail.stock:
        data.stock=product_detail.stock
    db.commit()
    db.refresh(data)
    return {"message":"Product details updated successfully","data":data}

def delete_product_info(product_detail,db):
    try:
        db.delete(product_detail)
        db.commit()
        return{'message':"product deleted Successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

