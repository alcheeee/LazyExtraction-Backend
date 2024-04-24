from sqlmodel import Session, select
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from ..models.models import User
from ..models.corp_models import Corporations
from ..auth.auth_handler import get_current_user
from ..database.db import get_session
from ..database.UserCRUD import user_crud
from app.game_systems.corporations.CorporationCRUD import CorpManager


corporation_router = APIRouter(
    prefix="/corporations",
    tags=["corporations"],
    responses={404: {"description": "Not Found"}}
)


@corporation_router.post("/create-corporation/{name}/{type}")
def create_corporation(name: str, type: str,
                       session: Session = Depends(get_session),
                       user: User = Depends(get_current_user)):
    try:
        corp_manager = CorpManager(session)
        result = corp_manager.create_corporation(name, type, user.id)
        return {"message": result}

    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail={"message": str(e)})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail={"message": "Error creating Corporation"})


@corporation_router.post("/add-user/{user_id_to_add:int}")
def add_user_to_corporation(user_id_to_add: int,
                            session: Session = Depends(get_session),
                            user: User = Depends(get_current_user)):

    corp_manager = CorpManager(session)
    corporation = session.get(Corporations, user.corp_id)

    if not corporation:
        raise HTTPException(status_code=404, detail="No associated corporation found.")
    if user.username != corporation.leader:
        raise HTTPException(status_code=403, detail="You are not authorized to add users.")

    target_user = session.get(User, user_id_to_add)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    success, msg = corp_manager.add_user_to_corporation(user_id_to_add, user.corp_id)
    if not success:
        raise HTTPException(status_code=400, detail=msg)

    return {"message": msg}


@corporation_router.post("/remove-user/{username_to_remove}")
def remove_user_from_corporation(user_id_to_remove: int,
                                 session: Session = Depends(get_session),
                                 user: User = Depends(get_current_user)):
    corp_manage = CorpManager(session)
    corporation = session.get(Corporations, user.corp_id)
    if not corporation:
        raise HTTPException(status_code=400, detail={"message": "Invalid Request"})

    if not user.username == corporation.leader:
        raise HTTPException(status_code=403, detail="You are not authorized to remove users.")

    target_user = user_crud.get_user_by_id(user_id_to_remove)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    success, msg = corp_manage.remove_user_from_corporation(user_id_to_remove, user.corp_id)
    if not success:
        raise HTTPException(status_code=400, detail=msg)

    return {"message": msg}


