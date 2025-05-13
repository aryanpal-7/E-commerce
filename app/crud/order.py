from app.models.orders import OrderModel
from app.crud.products import update_product_info
from app.schemas.product_schema import ProductDetails
from app.models.products import ProductModel
from app.schemas.order_schema import OrderOutput
from app.models.carts import CartModel
from sqlalchemy.orm import Session


def add_order(product_data: ProductModel, user_data, quantity, db):
    data = OrderModel(
        product_id=product_data.id,
        product_name=product_data.product_name,
        quantity=quantity,
        price=product_data.price,
        seller_name=product_data.admin.name,
        owner_id=user_data.id,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    # newStock = product_data.stock - quantity
    # update_product_info(
    #     product_detail=ProductDetails(
    #         product_name=product_data.product_name,
    #         price=product_data.price,
    #         stock=newStock,
    #     ),
    #     data=product_data,
    #     db=db,
    # )
    return {
        "message": "Order Placed Successfully",
        "order_details": OrderOutput.model_validate(data),
    }


def delete_order(data: OrderModel, db):
    db.delete(data)
    db.commit()
    return {"message": "Order Cancelled."}


def add_ordered_cart_items(stock_available, stock_unavailable, user, db: Session):
    order = []
    order_data = (
        db.query(CartModel)
        .filter(
            CartModel.product_id.in_(item.id for item in stock_available),
            CartModel.owner_id == user.id,
        )
        .all()
    )
    cart_map = {q.product_id: q.quantity for q in order_data}

    for item in stock_available:
        order.append(
            OrderModel(
                product_name=item.product_name,
                quantity=cart_map.get(item.id, 0),
                price=item.price,
                seller_name=item.admin.name,
                owner_id=user.id,
                product_id=item.id,
            )
        )
    db.add_all(order)
    product_ids = [item.id for item in stock_available]
    db.query(CartModel).filter(
        CartModel.product_id.in_(product_ids), CartModel.owner_id == user.id
    ).delete(synchronize_session=False)
    db.commit()
    for o in order:
        db.refresh(o)

    unavailable_stock = {p.product_name for p in stock_unavailable}

    return {
        "order": order,
        "stock_unavailable_products": (
            list(unavailable_stock) if stock_unavailable else []
        ),
    }
