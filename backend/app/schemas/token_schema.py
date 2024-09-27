from pydantic import BaseModel


class TokenData(BaseModel):
    username: str | None = None
    user_id: str | None = None

