from app.models.orders import OrderModel
from app.models.users import UserModel
from app.crud.products import update_product_info
from app.schemas.product_schema import ProductDetails
from app.models.products import ProductModel
from app.schemas.order_schema import OrderOutput
from app.models.carts import CartModel
from sqlalchemy.orm import Session
from typing import List


def add_order(
    product_data: ProductModel, user_data: UserModel, quantity: int, db: Session
) -> dict[str, str]:
    """
    Function to add an order in the database.

    Args:
        product_data (ProductModel): The product object to be ordered.
        user_data (UserModel): The user object who is placing the order.
        quantity (int): The quantity of the product being ordered.
        db (Session): The database session.

    Returns:
        dict[str, str]: A dictionary with a success message.
    """
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
    return {"message": "Order Placed Successfully"}


def delete_order(data: OrderModel, db: Session) -> dict[str, str]:
    """
    Function to delete an order from the database.

    Args:
        data (OrderModel): The order object to be deleted.
        db (Session): The database session.

    Returns:
        dict[str, str]: A dictionary with a success message.
    """
    db.delete(data)
    db.commit()
    return {"message": "Order Cancelled."}


def add_ordered_cart_items(
    stock_available: List[ProductModel],
    stock_unavailable: List[ProductModel],
    user: UserModel,
    db: Session,
):
    """
    Function to add ordered cart items to the orders table and remove the items from the cart table.

    Args:
        stock_available (List[ProductModel]): A list of products that are available in stock.
        stock_unavailable (List[ProductModel]): A list of products that are not available in stock.
        user (UserModel): The user model object.
        db (Session): The database session.

    Returns:
        dict: A dictionary with the order objects and a list of unavailable products.
    """
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
