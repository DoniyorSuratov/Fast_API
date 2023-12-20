from datetime import datetime
from typing import List
from pydantic import BaseModel


class MainProductsScheme(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    status: str
    category: str
    user_id: int


class AboutProductsScheme(BaseModel):
    version: str | None
    updated_at: datetime | None
    frameworks: str | None
    compatible_with: str | None
    tags: str | None
    name:str | None
    created_at: datetime | None

