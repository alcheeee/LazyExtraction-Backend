from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel, EmailStr
from ..models.models import User
from ..auth.auth_handler import token_handler, UserService
from ..crud.BaseCRUD import BaseCRUD
from ..database.db import get_session
from ..database.UserHandler import UserHandler

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
    async with get_session() as session:
        user_crud = BaseCRUD(model=User, session=session)
        exists = await user_crud.check_fields_exist(username=request.username, email=request.email)
        if exists:
            raise HTTPException(status_code=400, detail="User with that username or email already exists")

        user_handler = UserHandler(session=session)
        try:
            result = await user_handler.create_user(request.username, request.password, request.email)
            return {"message": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail={"message": "Internal Server Error"})


@user_router.post("/login")
async def login_for_access_token(username: str = Form(...),
                                 password: str = Form(...)):
    async with get_session() as session:
        auth_service = UserService(session=session)
        user_id = await auth_service.authenticate_user(username, password)
        if not user_id:
            raise HTTPException(status_code=400, detail={"message": "Incorrect username or password"})

        access_token = token_handler.create_token(user_id=user_id)
        return {"access_token": access_token, "token_type": "bearer"}







