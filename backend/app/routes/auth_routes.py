from fastapi import APIRouter, Form, Depends
from pydantic import BaseModel, EmailStr
from ..models.models import User
from ..auth.auth_handler import token_handler, UserService
from ..crud.BaseCRUD import BaseCRUD
from ..database.UserHandler import UserHandler
from . import dependency_session, ResponseBuilder, MyLogger, common_http_errors, AsyncSession
user_log = MyLogger.user()

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
async def register_new_user(
        request: UserCreateRequest,
        session: AsyncSession = Depends(dependency_session)
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
        session: AsyncSession = Depends(dependency_session)
    ):
    auth_service = UserService(session=session)
    user_id = await auth_service.authenticate_user(username, password)
    if not user_id:
        raise common_http_errors.mechanics_error("Incorrect username or password")

    access_token = token_handler.create_token(user_id=user_id)
    return {"access_token": access_token, "token_type": "bearer"}







