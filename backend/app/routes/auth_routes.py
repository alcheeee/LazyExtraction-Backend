from fastapi import APIRouter, Form, Depends
from pydantic import BaseModel, EmailStr

from ..auth.auth_handler import token_handler, UserService
from ..database.user_handler import UserHandler

from ..crud import BaseCRUD
from ..models import User
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    MyLogger,
    common_http_errors
)


user_log = MyLogger.user()
error_log = MyLogger.errors()


user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not Found"}}
)


@user_router.get("/")
async def root():
    return {"message": "User Router Ready"}


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: EmailStr


@user_router.post("/register")
async def register_new_user(
        request: UserCreateRequest,
        session: AsyncSession = Depends(get_db)
):
    user_crud = BaseCRUD(model=User, session=session)
    exists = await user_crud.check_fields_exist(username=request.username, email=request.email)
    if exists:
        raise common_http_errors.mechanics_error("User with that username or email already exists")

    user_handler = UserHandler(session=session)
    try:
        result = await user_handler.create_user(request.username, request.password, request.email)
        user_log.info(f"New User: {request.username}")
        return ResponseBuilder.success(result)

    except Exception as e:
        await session.rollback()
        raise common_http_errors.server_error()


@user_router.post("/login")
async def login_for_access_token(
        username: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_db)
):
    auth_service = UserService(session=session)
    user_id = await auth_service.authenticate_user(username, password)
    if not user_id:
        raise common_http_errors.mechanics_error("Incorrect username or password")

    access_token = await token_handler.create_token(user_id=user_id)
    return {"access_token": access_token, "token_type": "bearer"}





