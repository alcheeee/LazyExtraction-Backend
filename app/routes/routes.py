from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import BaseModel
from ..models.models import User
from ..auth.auth_handler import oauth2_scheme, get_current_user, UserAuthenticator
from .router_ids  import user_crud, RouteIDs, corporation_manager as corp_manager

authenticator = UserAuthenticator(user_data_manager=user_crud)
router = APIRouter()

class StatusCodes:
    ERROR_CODE = 400
    UNAUTHORIZED = 401
    SUCCESS_OK = 200



class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str

@router.post("/users/")
def register_new_user(user_request: UserCreateRequest):
    result, msg = user_crud.create_user(user_request.username, user_request.password, user_request.email)
    if result:
        return {"message": msg}
    else:
        raise HTTPException(status_code=StatusCodes.ERROR_CODE, detail=msg)



@router.post("/login")
def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    user = authenticator.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.StatusCodes.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = authenticator.create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}



class UserActionRequest(BaseModel):
    button_id: str

@router.post("/user-action")
async def user_action_buttons(request: UserActionRequest, user: User = Depends(get_current_user)):
    route_id = RouteIDs(request.button_id, user)
    result, msg = route_id.find_id()
    if result:
        return {"message": msg}
    else:
        raise HTTPException(status_code=StatusCodes.ERROR_CODE, detail=msg)



@router.post("/corporations/create-corporation")
def create_corporation(corporation_name: str = Form(...), corporation_type: str = Form(...), user: User = Depends(get_current_user)):
    result, msg = corp_manager.create_corporation(corporation_name, corporation_type, user.id)
    if result:
        return {"message": msg}
    else:
        raise HTTPException(status_code=StatusCodes.ERROR_CODE, detail=msg)




@router.post("/corporations/add-user")
def add_user_to_corporation(username_to_add_corporation: str = Form(...), user: User = Depends(get_current_user)):
    corporation = corp_manager.get_corp_from_user(user.id)
    if corporation.leader == user.username:
        result, msg = corp_manager.add_user_to_corporation(username_to_add_corporation, user.corp_id)
        return {"message": msg}
    else:
        msg = "You are not high enough in the Corporation to do that!"
        raise HTTPException(status_code=StatusCodes.ERROR_CODE, detail=msg)











