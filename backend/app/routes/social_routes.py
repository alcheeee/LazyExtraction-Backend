from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import SQLModel, select, Field, Relationship
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Query
from ..models.models import User, FriendsLink, FriendRequest, PrivateMessage
from ..auth.auth_handler import get_current_user
from ..database.db import get_session
from ..utils.logger import MyLogger
admin_log = MyLogger.admin()

social_router = APIRouter(
    prefix="/social",
    tags=["social"],
    responses={404: {"description": "Not Found"}}
)


@social_router.post("/send-friend-request/{target_user_id}")
async def send_friend_request(target_user_id: int, user: User = Depends(get_current_user)):

    async with get_session() as session:
        target_user = await session.get(User, target_user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.id == target_user_id:
            raise HTTPException(status_code=400, detail="Cannot send friend request to yourself")

        friend_request = (await session.execute(
            select(FriendRequest).where(
                (FriendRequest.requester_id == user.id) &
                (FriendRequest.requestee_id == target_user_id) &
                (FriendRequest.status == "pending")
            ))).scalars().first()
        if friend_request:
            raise HTTPException(status_code=400, detail="Friend request already sent or pending")

        try:
            new_request = FriendRequest(requester_id=user.id, requestee_id=target_user.id)
            session.add(new_request)
            await session.commit()
            return {"message": "Friend request sent successfully"}
        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=400, detail={"message": "Failed to send friend request"})


@social_router.delete("/remove-friend/{friend_id}")
async def remove_friend(friend_id: int, user: User = Depends(get_current_user)):
    async with get_session() as session:
        friendship = (await session.execute(
            select(FriendsLink).where(
            ((FriendsLink.user1_id == user.id) & (FriendsLink.user2_id == friend_id)) |
            ((FriendsLink.user1_id == friend_id) & (FriendsLink.user2_id == user.id))
        ))).scalars().all()

        if not friendship:
            raise HTTPException(status_code=404, detail="Friend not found")
        try:
            await session.delete(friendship)
            await session.commit()
            return {"message": "Friend successfully removed"}
        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=500, detail="Error removing friend")


@social_router.post("/respond-friend-request/{request_user_id}")
async def respond_friend_request(request_user_id: int,
                                 response: str,
                                 user: User = Depends(get_current_user)):

    async with get_session() as session:
        try:
            friend_request = await session.get(FriendRequest, request_user_id)
            if not friend_request:
                raise HTTPException(status_code=404, detail="Friend request not found")
            if friend_request.requestee_id != user.id:
                raise HTTPException(status_code=403, detail="Unauthorized to respond to this friend request")
            if response == 'accept':
                friend_request.status = 'accepted'
            elif response == 'decline':
                friend_request.status = 'declined'
            else:
                raise HTTPException(status_code=400, detail="Invalid response. Choose 'accept' or 'decline'.")

            await session.commit()
            return {"message": f"Friend request {friend_request.status}"}

        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=400, detail={"message": "Failed to respond to friend request"})

class MessageCreate(BaseModel):
    content: str

@social_router.post("/send-message/{receiver_id}")
async def send_message(receiver_id: int,
                     message_data: MessageCreate,
                     user: User = Depends(get_current_user)):

    async with get_session() as session:
        friends_link = (await session.execute(
            select(FriendsLink).where(
            ((FriendsLink.user1_id == user.id) & (FriendsLink.user2_id == receiver_id)) |
            ((FriendsLink.user1_id == receiver_id) & (FriendsLink.user2_id == user.id))
        ))).scalars().all()

        if not friends_link:
            raise HTTPException(status_code=403, detail="Users are not friends")

        try:
            new_message = PrivateMessage(sender_id=user.id, receiver_id=receiver_id, content=message_data.content)
            session.add(new_message)
            await session.commit()
            return {"message": "Message sent successfully"}
        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=400, detail={"message": "Failed to send message"})


@social_router.get("/friend-requests/")
async def get_friend_requests(user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            friend_requests = (await session.execute(
                select(FriendRequest)
                .where(
                    FriendRequest.requestee_id == user.id)
                .where(
                    FriendRequest.status == "pending")
            )).scalars().all()

            return [{"friends_id": fr.id,
                     "from": fr.requester_id,
                     "status": fr.status,
                     "created_at": fr.created_at}
                    for fr in friend_requests]
        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=400, detail={"message": str(e)})


@social_router.get("/friends/")
async def get_friends(user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            friend_links = (await session.execute(
                select(FriendsLink).where(
                    (FriendsLink.user1_id == user.id) |
                    (FriendsLink.user2_id == user.id)
                ))).scalars().all()

            friend_ids = {fr.user1_id if fr.user1_id != user.id else fr.user2_id for fr in friend_links}
            if friend_ids:
                friends_info = (await session.execute(
                    select(User).where(
                        User.id.in_(friend_ids))
                )).scalars().all()
                return [{"friends_id": friend.id, "username": friend.username} for friend in friends_info]
            else:
                return []
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": "Failed to load friends"})


@social_router.get("/messages/")
async def get_messages(user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            messages = (await session.execute(
                select(PrivateMessage).where(
                    (PrivateMessage.sender_id == user.id) |
                    (PrivateMessage.receiver_id == user.id))
                .order_by(PrivateMessage.timestamp.desc())
            )).scalars().all()

            if not messages:
                return []

            user_ids = {msg.sender_id for msg in messages} | {msg.receiver_id for msg in messages}
            users = (await session.execute(
                select(User).where(
                    User.id.in_(user_ids))
            )).scalars().all()
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