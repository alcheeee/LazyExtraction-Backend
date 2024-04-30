from fastapi import APIRouter, HTTPException, Form, Depends
from pydantic import BaseModel, EmailStr
from ..auth.auth_handler import UserAuthenticator
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
    user_auth_crud = UserHandler()
    try:
        result = await user_auth_crud.create_user(request.username, request.password, request.email)
        return {"message": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "Internal Server Error"})


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







