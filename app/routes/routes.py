from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import BaseModel
from ..models.models import User
from ..auth.auth_handler import oauth2_scheme, get_current_user, UserAuthenticator
from .router_ids  import user_crud, RouteIDs

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
def create_user(user_request: UserCreateRequest):
    result, msg = user_crud.create_user(user_request.username, user_request.password, user_request.email)
    if result:
        return {"message": msg}
    else:
        raise HTTPException(status_code=StatusCodes.ERROR_CODE, detail=msg)



class LoginRequest(BaseModel):
    username: str
    password: str

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
async def adjust_energy(request: UserActionRequest, user: User = Depends(get_current_user)):
    route_id = RouteIDs(request.button_id, user)
    result, msg = route_id.find_id()
    if result:
        return {"message": "Action executed successfully", "Details": msg}
    else:
        raise HTTPException(status_code=StatusCodes.ERROR_CODE, detail=msg)

























