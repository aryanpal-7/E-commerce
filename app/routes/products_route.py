"""
1. Add Products Route only for admin roles. ~
2. Retrieve all Products.~
3. Update Product Details like stock etc.
4. Delete a Product.

"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductDetails, ProductOut
from app.core.database import get_db
from app.services.product_services import add_products, update_product, delete_product
from app.models.products import ProductModel
from app.core.security import get_current_user
from app.models.users import UserModel
from typing import List

router = APIRouter()


def check_admin(role):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only Admins are allowed."
        )


def validate_fields(product_name, price, stock):
    if not product_name or price < 0 or stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid details or Details are missing",
        )


@router.get("/products", response_model=List[ProductOut])
def get_all_product(
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    data = db.query(ProductModel).offset(offset).limit(limit).all()
    return data


@router.post("/addproducts")
def add_products_info(
    product_details: ProductDetails,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_admin(user.role)
    validate_fields(
        product_details.product_name, product_details.price, product_details.stock
    )
    return add_products(product_details, user.id, db)


@router.put("/updateproduct/{product_id}")
def update_product_info(
    product_id: int,
    product_details: ProductDetails,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_admin(user.role)
    validate_fields(
        product_details.product_name, product_details.price, product_details.stock
    )
    return update_product(product_details, product_id, db)


@router.delete("/deleteproduct/{product_id}")
def delete_product_info(
    product_id: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_admin(user.role)
    return delete_product(product_id, user, db)
