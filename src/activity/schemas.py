from datetime import datetime

from pydantic import BaseModel


class ActivityBase(BaseModel):
    username: str


class LikeActivityCreate(ActivityBase):
    liked_post_id: int
    username_like: str


class FollowActivityCreate(ActivityBase):
    followed_username: str


class Activity(ActivityBase):
    timestamp: datetime

    class Config:
        orm_mode = True
