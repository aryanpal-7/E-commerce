from fastapi import APIRouter, FastAPI
from app.routes.user_route import router as UserRouter

app = FastAPI()


app.include_router(UserRouter, tags=["This is the User Router."])
