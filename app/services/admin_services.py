from fastapi import status, HTTPException
from app.models.users import UserModel
from app.crud.users import add_user
def register_admin(admin_data,db):
    data=db.query(UserModel).filter(UserModel.email==admin_data.email, UserModel.role=="admin").first()
    if data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admin Already Exists.")
    return add_user(admin_data,db)
    
