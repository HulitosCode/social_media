from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Hashtag(BaseModel):
    id: int
    name: str


class PostCreate(BaseModel):
    content: Optional[str] = None
    image: str
    location: Optional[str] = None


class Post(PostCreate):
    id: int
    author_id: int
    likes_count: int
    created_at: datetime

    class Config:
        orm_mode = True
