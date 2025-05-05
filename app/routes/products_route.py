"""
    1. Add Products Route only for admin roles. ~
    2. Retrieve all Products.~
    3. Update Product Details like stock etc. 
    4. Delete a Product.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from app.schemas.product_schema import ProductDetails
from app.core.database import get_db
from app.services.product_services import add_products, update_product, delete_product
from app.models.products import ProductModel
router=APIRouter()

@router.get("/products")
def get_all_product(db:Session=Depends(get_db)):
    return db.query(ProductModel).all()

@router.post("/addproducts")
def add_products_info(product_details:ProductDetails,db:Session=Depends(get_db)):
    if not product_details.product_name or not product_details.price or not product_details.stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Details are missing")
    return add_products(product_details,db)
    

@router.put("/updateproduct/{product_id}")
def update_product_info(product_id:int,product_details:ProductDetails, db:Session=Depends(get_db)):
    if not product_details.product_name or not product_details.price or not product_details.stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Details are missing")
    return update_product(product_details,product_id,db)
    

@router.delete("/deleteproduct/{product_id}")
def delete_product_info(product_id:int,db:Session=Depends(get_db)):
    if not product_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID missing.")
    return delete_product(product_id,db)