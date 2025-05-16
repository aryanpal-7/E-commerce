from fastapi import FastAPI
from app.routes.user_route import router as UserRouter
from app.routes.products_route import router as ProductRouter
from app.routes.admin_route import router as AdminRouter
from app.routes.cart_route import router as CartRouter
from app.routes.order_route import router as OrderRouter

app = FastAPI()


app.include_router(UserRouter, prefix="/users", tags=["Users Routes."])
app.include_router(ProductRouter, prefix="/products", tags=["Product Routes."])
app.include_router(AdminRouter, prefix="/admin", tags=["Admin Routes."])
app.include_router(CartRouter, prefix="/cart", tags=["Cart Routes."])
app.include_router(OrderRouter, prefix="/order", tags=["Order Routes."])
