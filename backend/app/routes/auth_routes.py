from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Form, Depends, HTTPException
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
    email: Optional[EmailStr | None]
    guest_account: Optional[bool] = False


@user_router.post("/register")
@exception_decorator
async def register_new_user(
        request: UserCreateRequest,
        session: AsyncSession = Depends(get_db)
):
    if request.guest_account is True and request.email is not None:
        raise ValueError("You're not supposed to be doing that")

    elif request.guest_account is False and request.email is None:
        raise ValueError("You're not supposed to be doing that")

    #elif request.guest_account:
        # TODO : Add Guest Account logic,
        #  Name change logic (New Column, name_changes: int, start with 1 if guest_account)
        #  else 0, costs $x to change


    if len(request.username) < 4:
        raise ValueError("Minimum name length is 4.")
    if len(request.password) < 6:
        raise ValueError("Please use a longer password.")

    user_crud = BaseCRUD(model=User, session=session)
    if request.guest_account is True:
        exists = await user_crud.check_fields_exist(username=request.username)

    elif request.guest_account is False and request.email is not None:
        exists = await user_crud.check_fields_exist(username=request.username, email=request.email)
    else:
        raise ValueError("An error occurred while creating the account")

    if exists:
        raise ValueError("User with that username or email already exists")

    user_handler = UserHandler(session=session)
    new_data = await user_handler.create_user(
        request.username,
        request.password,
        request.email if request.email else None,
        guest_account=request.guest_account
    )
    user_log.info(f"New User: {request.username} {request.email}")
    return ResponseBuilder.success(f"Account created successfully! Welcome {request.username}", data=new_data)


@user_router.post("/login")
@exception_decorator
async def login_for_access_token(
        username: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_db)
):
    auth_service = UserService(session=session)
    user_id = await auth_service.authenticate_user(username, password)
    if not user_id:
        raise ValueError("Incorrect username or password")

    access_token, refresh_token = UserHandler.create_tokens(username, user_id)

    return JSONResponse(
        content={
            "message": "Login Successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )


@user_router.post("/refresh-token")
@exception_decorator
async def get_new_access_token(token_data: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_data['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = TokenHandler.create_access_token(
            user_data=token_data['user']
        )

        return JSONResponse(content={
            "access_token": new_access_token
        })

    raise CommonHTTPErrors.credentials_error(message="Invalid or expired login", data=token_data)


@user_router.post("/test/test-token")
@exception_decorator
async def access_token_test(user_data: dict = Depends(AccessTokenBearer())):
    if not settings.TESTING:
        raise HTTPException(status_code=418)
    return ResponseBuilder.success("Token Valid")

