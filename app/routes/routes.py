from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..models.models import User
from ..auth.auth_handler import oauth2_scheme,user_crud, get_current_user


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



class EnergyAdjustRequest(BaseModel):
    energy_delta: int


@router.post("/energy/adjust")
async def adjust_energy(request: EnergyAdjustRequest, user: User = Depends(get_current_user)):
    result, msg = user_crud.adjust_energy(user.id, request.energy_delta)
    if result:
        return {"message": "Energy adjusted successfully", "Energy Adjusted": msg}
    else:
        # You might want to customize this message based on the actual reason of failure
        raise HTTPException(status_code=400, detail=msg)