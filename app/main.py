from fastapi import FastAPI
from app.routes.user_route import router as UserRouter
from app.routes.products_route import router as ProductRouter
from app.routes.admin_route import router as AdminRouter
app = FastAPI()


app.include_router(UserRouter, tags=["These are the Users Routes."])
app.include_router(ProductRouter, tags=["These are the Product Routes"])
app.include_router(AdminRouter, tags=["These are the Admin Routes."])