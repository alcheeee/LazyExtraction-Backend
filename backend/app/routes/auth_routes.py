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
    common_http_errors,
    exception_decorator
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
    return ResponseBuilder.success("User routes ready")


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: EmailStr


@user_router.post("/register")
@exception_decorator
async def register_new_user(
        request: UserCreateRequest,
        session: AsyncSession = Depends(get_db)
):
    if len(request.username) < 4:
        raise ValueError("Minimum name length is 4.")
    if len(request.password) < 6:
        raise ValueError("Please use a longer password.")
    user_crud = BaseCRUD(model=User, session=session)
    exists = await user_crud.check_fields_exist(username=request.username, email=request.email)
    if exists:
        raise ValueError("User with that username or email already exists")

    user_handler = UserHandler(session=session)
    result = await user_handler.create_user(request.username, request.password, request.email)
    user_log.info(f"New User: {request.username}")
    return ResponseBuilder.success(result)


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





