from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, EmailStr

from app.settings import settings
from app.schemas.token_schema import TokenData
from app.auth.auth_handler import TokenHandler, UserService
from app.auth import AccessTokenBearer, RefreshTokenBearer

from app.database.user_handler import UserHandler
from app.crud import UserCRUD
from app.models import User
from . import (
	DataName,
	AsyncSession,
	error_responses,
	ResponseBuilder,
	MyLogger,
	CommonHTTPErrors,
	exception_decorator
)
from app.dependencies.get_db import get_db

user_log = MyLogger.user()
error_log = MyLogger.errors()

user_router = APIRouter(
	prefix="/user",
	tags=["user"],
	responses=error_responses
)


@user_router.get("/")
async def root():
	return ResponseBuilder.success(message="User routes ready")


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
	request.guest_account = True if not request.email else False
	request.email = None if request.guest_account else request.email

	# if request.guest_account:
	# TODO : Add Guest Account logic,
	#  Name change logic (New Column, name_changes: int, start with 1 if guest_account)
	#  else 0, costs $x to change

	if len(request.username) < 4:
		raise ValueError("Minimum name length is 4")
	if len(request.password) < 6:
		raise ValueError("Please use a longer password")

	user_crud = UserCRUD(model=User, session=session)
	if request.guest_account is True:
		exists = await user_crud.check_fields_exist(username=request.username)

	elif request.guest_account is False and request.email is not None:
		exists = await user_crud.check_fields_exist(username=request.username, email=request.email)
	else:
		raise ValueError("An error occurred while creating your account")

	if exists:
		raise ValueError("User with that username or email already exists")

	user_handler = UserHandler(session=session)
	new_data = await user_handler.create_user(
		username=request.username,
		password=request.password,
		email=request.email,
		guest_account=request.guest_account
	)
	user_log.info(f"New User: {request.username} {request.email}")
	return ResponseBuilder.success(
		f"Account created successfully! Welcome {request.username}",
		data_name=DataName.UserData, data=new_data
	)


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
	token_data = TokenData(username=username, user_id=str(user_id))
	access_token, refresh_token = await run_in_threadpool(UserHandler.create_tokens, token_data)
	return JSONResponse(content={
		"message": "Login Successful",
		"access_token": access_token,
		"refresh_token": refresh_token
	})


@user_router.post("/refresh-token")
@exception_decorator
async def get_new_access_token(user_data: dict = Depends(RefreshTokenBearer())):
	expiry_timestamp = user_data['exp']
	if datetime.fromtimestamp(expiry_timestamp) <= datetime.now():
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired login")

	new_token_data = TokenData(
		username=user_data['user']['username'],
		user_id=user_data['user']['user_id']
	)
	new_access_token = await run_in_threadpool(TokenHandler.create_access_token, token_data=new_token_data)

	return JSONResponse(content={
		"access_token": new_access_token
	})


@user_router.post("/test/test-token")
@exception_decorator
async def access_token_test(user_data: dict = Depends(AccessTokenBearer())):  # noqa
	if not settings.TESTING:
		raise HTTPException(status_code=418)
	return ResponseBuilder.success("Token Valid")
