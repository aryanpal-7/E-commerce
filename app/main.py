from fastapi import FastAPI
from app.routes.user_route import router as UserRouter
from app.routes.products_route import router as ProductRouter
from app.routes.admin_route import router as AdminRouter
from app.routes.cart_route import router as CartRouter

app = FastAPI()


app.include_router(UserRouter, tags=["Users Routes."])
app.include_router(ProductRouter, tags=["Product Routes"])
app.include_router(AdminRouter, tags=["Admin Routes."])
app.include_router(CartRouter, tags=["Cart Routes"])
