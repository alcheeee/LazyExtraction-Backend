from pydantic import BaseModel
from sqlmodel import select
from fastapi import APIRouter, Depends
from ..models.models import User, FriendsLink, FriendRequest, PrivateMessage
from ..auth import current_user
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    MyLogger,
    common_http_errors
)


error_log = MyLogger.errors()


social_router = APIRouter(
    prefix="/social",
    tags=["social"],
    responses={404: {"description": "Not Found"}}
)


@social_router.post("/send-friend-request/{target_user_id}")
async def send_friend_request(
        target_user_id: int,
        user: str = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
    ):
    target_user = await session.get(User, target_user_id)
    if not target_user:
        raise ValueError("User not found")

    if user.id == target_user_id:
        raise ValueError("Cannot send friend request to yourself")

    friend_request = (await session.execute(
        select(FriendRequest).where(
            (FriendRequest.requester_id == user.id) &
            (FriendRequest.requestee_id == target_user_id) &
            (FriendRequest.status == "pending")
        ))).scalars().first()
    if friend_request:
        raise ValueError("Friend request already sent or pending")
    try:
        new_request = FriendRequest(requester_id=user.id, requestee_id=target_user.id)
        session.add(new_request)
        await session.commit()
        msg = "Friend request sent successfully"
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        raise common_http_errors.mechanics_error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@social_router.delete("/remove-friend/{friend_id}")
async def remove_friend(
        friend_id: int,
        user: User = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
    ):
    friendship = (await session.execute(
        select(FriendsLink).where(
        ((FriendsLink.user1_id == user.id) & (FriendsLink.user2_id == friend_id)) |
        ((FriendsLink.user1_id == friend_id) & (FriendsLink.user2_id == user.id))
    ))).scalars().all()

    if not friendship:
        raise ValueError("Friend not found")
    try:
        await session.delete(friendship)
        await session.commit()
        msg = "Friend successfully removed"
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        raise common_http_errors.mechanics_error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@social_router.post("/respond-friend-request/{request_user_id}")
async def respond_friend_request(
        request_user_id: int,
        response: str,
        user: User = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
    ):
    try:
        friend_request = await session.get(FriendRequest, request_user_id)
        if not friend_request:
            raise ValueError("Friend request not found")
        if friend_request.requestee_id != user.id:
            raise ValueError("Unauthorized to respond to this friend request")
        if response == 'accept':
            friend_request.status = 'accepted'
        elif response == 'decline':
            friend_request.status = 'declined'
        else:
            raise ValueError("Invalid response. Choose 'accept' or 'decline'.")

        await session.commit()
        msg = f"Friend request {friend_request.status}"
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        raise common_http_errors.mechanics_error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


class MessageCreate(BaseModel):
    content: str


@social_router.post("/send-message/{receiver_id}")
async def send_message(
        receiver_id: int,
        message_data: MessageCreate,
        user: User = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
    ):

    friends_link = (await session.execute(
        select(FriendsLink).where(
        ((FriendsLink.user1_id == user.id) & (FriendsLink.user2_id == receiver_id)) |
        ((FriendsLink.user1_id == receiver_id) & (FriendsLink.user2_id == user.id))
    ))).scalars().all()

    if not friends_link:
        raise ValueError("Users are not friends")

    try:
        new_message = PrivateMessage(sender_id=user.id, receiver_id=receiver_id, content=message_data.content)
        session.add(new_message)
        await session.commit()
        msg = "Message sent successfully"
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        raise common_http_errors.mechanics_error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@social_router.get("/friend-requests/")
async def get_friend_requests(
        user: User = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
    ):
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

    except ValueError as e:
        await session.rollback()
        raise common_http_errors.mechanics_error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@social_router.get("/friends/")
async def get_friends(
        user: User = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
    ):
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
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@social_router.get("/messages/")
async def get_messages(
        user: User = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
    ):
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
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()
