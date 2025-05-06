from app.models.carts import CartModel


def add_product(user_id, quantity, product_id, db):
    data = CartModel(product_id=product_id, quantity=quantity, owner_id=user_id)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def delete_cart_product(data, db):
    db.delete(data)
    db.commit()
    # Update Stock in ProductModel.
    return {"message": "Data Deleted Successfully."}


def update_cart_details(data, quantity, db):
    data.quantity = quantity
    db.commit()
    db.refresh(data)
    return {"message": "Updated successfully", "data": data}
