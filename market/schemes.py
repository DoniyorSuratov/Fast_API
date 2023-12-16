from datetime import datetime
from typing import List
from pydantic import BaseModel

class MainProductsScheme(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    status: str
    category_id: int
    user_id: int

class AboutProductsScheme(BaseModel):
    version: str
    updated_at: datetime
    frameworks: str
    compatible_with: str
    tags: str
