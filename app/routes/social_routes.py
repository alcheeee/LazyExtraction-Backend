from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import SQLModel, Session, select, Field, Relationship
from fastapi import APIRouter, HTTPException, Depends
from ..models.models import User, FriendsLink, FriendRequest, PrivateMessage
from ..auth.auth_handler import get_current_user
from ..database.db import get_session

social_router = APIRouter(
    prefix="/social",
    tags=["social"],
    responses={404: {"description": "Not Found"}}
)


class UserSocialRequest(BaseModel):
    username: str

@social_router.post("/send-friend-request/")
def send_friend_request(request: UserSocialRequest,
                        session: Session = Depends(get_session),
                        user: User = Depends(get_current_user)):

    target_user = session.exec(select(User).where(User.username == request.username)).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if session.exec(select(FriendRequest).where(
        (FriendRequest.requester_id == user.id) &
        (FriendRequest.requestee_id == target_user.id) &
        (FriendRequest.status == "pending")
    )).first():
        raise HTTPException(status_code=400, detail="Friend request already sent or pending")

    try:
        new_request = FriendRequest(requester_id=user.id, requestee_id=target_user.id)
        session.add(new_request)
        session.commit()
        return {"message": "Friend request sent successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail={"message": "Failed to send friend request"})


@social_router.delete("/remove-friend/{friend_id}")
def remove_friend(friend_id: int,
                  session: Session = Depends(get_session),
                  user: User = Depends(get_current_user)):

    friendship = session.exec(select(FriendsLink).where(
        ((FriendsLink.user1_id == user.id) & (FriendsLink.user2_id == friend_id)) |
        ((FriendsLink.user1_id == friend_id) & (FriendsLink.user2_id == user.id))
    )).first()

    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    try:
        session.delete(friendship)
        session.commit()
        return {"message": "Friend successfully removed"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@social_router.post("/respond-friend-request/")
def respond_friend_request(request_user_id: int,
                           response: str,
                           session: Session = Depends(get_session),
                           user: User = Depends(get_current_user)):
    try:
        friend_request = session.get(FriendRequest, request_user_id)
        if not friend_request or friend_request.requestee_id != user.id:
            raise HTTPException(status_code=404, detail="Friend request not found or access denied")

        if response not in ["accept", "decline"]:
            raise HTTPException(status_code=400, detail="Invalid response type")

        if response == "accept":
            friend_request.status = "accepted"
            existing_link = session.exec(select(FriendsLink).where(
                ((FriendsLink.user1_id == user.id) & (FriendsLink.user2_id == friend_request.requester_id)) |
                ((FriendsLink.user1_id == friend_request.requester_id) & (FriendsLink.user2_id == user.id))
            )).first()

            if not existing_link:
                new_link = FriendsLink(user1_id=user.id, user2_id=friend_request.requester_id)
                session.add(new_link)
            else:
                raise HTTPException(status_code=409, detail="Friendship already exists")
        else:
            friend_request.status = "declined"

        session.commit()
        return {"message": f"Friend request {response}"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail={"message": "Failed to respond to friend request"})

@social_router.post("/send-message/")
def send_message(receiver_id: int, content: str,
                 session: Session = Depends(get_session),
                 user: User = Depends(get_current_user)):

    if not session.exec(select(FriendsLink).where(
        ((FriendsLink.user1_id == user.id) & (FriendsLink.user2_id == receiver_id)) |
        ((FriendsLink.user1_id == receiver_id) & (FriendsLink.user2_id == user.id))
    )).first():
        raise HTTPException(status_code=403, detail="Users are not friends")

    try:
        new_message = PrivateMessage(sender_id=user.id, receiver_id=receiver_id, content=content)
        session.add(new_message)
        session.commit()
        return {"message": "Message sent successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail={"message": "Failed to send message"})


@social_router.get("/friend-requests/")
def get_friend_requests(session: Session = Depends(get_session),
                        user: User = Depends(get_current_user)):
    try:
        friend_requests = session.exec(select(FriendRequest)
                                       .where(FriendRequest.requestee_id == user.id)
                                       .where(FriendRequest.status == "pending")).all()
        return [{"friends_id": fr.id,
                 "from": fr.requester_id,
                 "status": fr.status,
                 "created_at": fr.created_at
                 }
                for fr in friend_requests]
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail={"message": str(e)})


@social_router.get("/friends/")
def get_friends(session: Session = Depends(get_session),
                user: User = Depends(get_current_user)):
    try:
        friend_links = session.exec(select(FriendsLink)
                                    .where((FriendsLink.user1_id == user.id) | (FriendsLink.user2_id == user.id))).all()

        friend_ids = {fr.user1_id if fr.user1_id != user.id else fr.user2_id for fr in friend_links}
        if friend_ids:
            friends_info = session.exec(select(User).where(User.id.in_(friend_ids))).all()
            return [{"friends_id": friend.id, "username": friend.username} for friend in friends_info]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": "Failed to load friends"})


@social_router.get("/messages/")
def get_messages(session: Session = Depends(get_session),
                 user: User = Depends(get_current_user)):
    try:
        messages = session.exec(select(PrivateMessage)
                                .where((PrivateMessage.sender_id == user.id) | (PrivateMessage.receiver_id == user.id))
                                .order_by(PrivateMessage.timestamp.desc())).all()
        if not messages:
            return []

        user_ids = {msg.sender_id for msg in messages} | {msg.receiver_id for msg in messages}
        users = session.exec(select(User).where(User.id.in_(user_ids))).all()
        user_dict = {user.id: user.username for user in users}

        messages_info = [{
            "id": msg.id,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "sender": user_dict.get(msg.sender_id),
            "receiver": user_dict.get(msg.receiver_id)
        } for msg in messages]
        return messages_info
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": "Failed to load messages"})
