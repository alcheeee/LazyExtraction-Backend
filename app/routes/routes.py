from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import BaseModel
from ..models.models import User
from ..auth.auth_handler import oauth2_scheme, get_current_user, UserAuthenticator
from .router_ids import user_crud, RouteIDs

authenticator = UserAuthenticator(user_data_manager=user_crud)

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not Found"}}
)


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str

@user_router.post("/register")
def register_new_user(user_request: UserCreateRequest):
    result, msg = user_crud.create_user(user_request.username, user_request.password, user_request.email)
    if result:
        return {"message": msg}
    else:
        raise HTTPException(status_code=400, detail={"message": msg})



@user_router.post("/login")
def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    user = authenticator.authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail={"message": "Incorrect username or password"})

    access_token = authenticator.create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}



class UserActionRequest(BaseModel):
    button_id: str

@user_router.post("/user-action")
async def user_action_buttons(request: UserActionRequest, user: User = Depends(get_current_user)):
    route_id = RouteIDs(request.button_id, user)
    result, msg = route_id.find_id()
    if result:
        return {"message": msg}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": msg})







