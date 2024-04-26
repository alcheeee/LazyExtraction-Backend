from fastapi import APIRouter, HTTPException, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from ..auth.auth_handler import UserService
from ..auth.auth_handler import UserAuthenticator
from app.database.CRUD.BaseCRUD import EnhancedCRUD
from ..database.db import get_session
from ..database.UserHandler import user_crud


user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not Found"}}
)


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: EmailStr

@user_router.post("/register")
async def register_new_user(request: UserCreateRequest):
    result, msg = await user_crud.create_user(request.username, request.password, request.email)
    if result:
        return {"message": msg}
    else:
        raise HTTPException(status_code=400, detail={"message": msg})


@user_router.post("/login")
async def login_for_access_token(username: str = Form(...),
                                 password: str = Form(...)):
    async with get_session() as session:
        user_auth = UserAuthenticator()
        user = await user_auth.authenticate_user(username, password, session=session)
        if not user:
            raise HTTPException(status_code=400, detail={"message": "Incorrect username or password"})

        access_token = user_auth.create_access_token(user_id=user.id)
        return {"access_token": access_token, "token_type": "bearer"}







