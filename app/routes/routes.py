from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import BaseModel
from ..models.models import User
from ..auth.auth_handler import oauth2_scheme,user_crud, get_current_user, UserAuthenticator

authenticator = UserAuthenticator(user_data_manager=user_crud)
router = APIRouter()

class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str


@router.post("/users/")
def create_user(user_request: UserCreateRequest):
    result = user_crud.create_user(user_request.username, user_request.password, user_request.email)
    if result:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Error creating user")


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    user = authenticator.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = authenticator.create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


class EnergyAdjustRequest(BaseModel):
    energy_delta: int


@router.post("/energy/adjust")
async def adjust_energy(request: EnergyAdjustRequest, user: User = Depends(get_current_user)):
    result, msg = user_crud.adjust_energy(user.id, request.energy_delta)
    if result:
        return {"message": "Energy adjusted successfully", "Energy Adjusted": msg}
    else:
        raise HTTPException(status_code=400, detail=msg)