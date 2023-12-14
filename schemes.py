from datetime import datetime

from pydantic import BaseModel


class Blog(BaseModel):
    id: int
    title: str
    description: str
    created_date: datetime
    is_active: bool
    view_count: int


class BlogPost(BaseModel):
    title: str
    description: str
