from fastapi import APIRouter, HTTPException, Depends, Form, status
from ..models.models import User
from ..auth.auth_handler import get_current_user
from app.game_systems.corporations.CorporationCRUD import corporation_manager as corp_manager

corporation_router = APIRouter(
    prefix="/corporations",
    tags=["corporations"],
    responses={404: {"description": "Not Found"}}
)



@corporation_router.post("/create-corporation")
def create_corporation(corporation_name: str = Form(...), corporation_type: str = Form(...), user: User = Depends(get_current_user)):
    result, msg = corp_manager.create_corporation(corporation_name, corporation_type, user.id)
    if result:
        return {"message": msg}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": msg})



@corporation_router.post("/add-user")
def add_user_to_corporation(username_to_add: str = Form(...), user: User = Depends(get_current_user)):
    corporation = corp_manager.get_corp_from_user(user.id)
    if not corporation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Invalid Request"})
    if str(corporation.leader) == user.username:
        result, msg = corp_manager.add_user_to_corporation(username_to_add, user.corp_id)
        return {"message": msg}
    else:
        msg = "You are not high enough in the Corporation to do that!"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": msg})



@corporation_router.post("/remove-user")
def remove_user_from_corporation(username_to_remove: str = Form(...), user: User = Depends(get_current_user)):
    corporation = corp_manager.get_corp_from_user(user.id)
    if not corporation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Invalid Request"})
    if str(corporation.leader) == user.username:
        result, msg = corp_manager.remove_user_from_corporation(username_to_remove, user.corp_id)
        return {"message": msg}
    else:
        msg = "You are not high enough in the Corporation to do that!"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": msg})