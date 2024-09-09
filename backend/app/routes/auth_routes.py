from datetime import datetime, timedelta

from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from ..config import settings
from ..auth.auth_handler import TokenHandler, UserService
from ..auth import AccessTokenBearer, RefreshTokenBearer
from ..database.user_handler import UserHandler

from ..crud import BaseCRUD
from ..models import User
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    MyLogger,
    CommonHTTPErrors,
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
        raise CommonHTTPErrors.mechanics_error("Incorrect username or password")

    user_data = {"username": username, "user_id": str(user_id)}
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = TokenHandler.create_access_token(
        user_data=user_data,
        expires_delta=access_token_expires
    )
    refresh_token = TokenHandler.create_access_token(
        user_data=user_data,
        expires_delta=refresh_token_expires,
        refresh=True
    )

    return JSONResponse(
        content={
            "message": "Login Successful",
            "access_token": access_token,
            "refresh_token": refresh_token
            #"user": {
            #    "username": username,
            #    "user_id": str(user_id)
            #}
        }
    )


@user_router.post("/refresh-token")
async def get_new_access_token(token_data: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_data['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = TokenHandler.create_access_token(
            user_data=token_data['user']
        )

        return JSONResponse(content={
            "access_token": new_access_token
        })

    raise CommonHTTPErrors.credentials_error(message="Invalid or expired login")


@user_router.post("/test/expired-token-test")
async def expired_token_test(user_data: dict = Depends(AccessTokenBearer())):
    return ResponseBuilder.success("Token Valid")

