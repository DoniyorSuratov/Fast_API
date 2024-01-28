from datetime import datetime
from typing import List
from sqlalchemy import text
from sqlalchemy.dialects.oracle import oracledb

from auth.schemes import UserInfo
from pydantic import BaseModel, Field
from fastapi import UploadFile, Query


class MainProductsScheme(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    status: str
    category: str = ""
    user_id: int
    image: str = None


class AboutProductsScheme(BaseModel):
    version: str = None
    updated_at: datetime = None
    frameworks: str = None
    compatible_with: str = None
    tags: str = None
    name: str = None
    created_at: datetime = None
    image: str = None


class CartAddProductsScheme(BaseModel):
    product_id:int


class CartShowProductsScheme(BaseModel):
    owner_id: int
    product_info: dict
    license: str


class BlogScheme(BaseModel):
    title: str
    description: str


class BlogGETScheme(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    blog_owner: UserInfo


class AddProductScheme(BaseModel):
    frameworks: str
    compatible_with: str
    tags: str
    name: str
    description: str
    category_id: int
    version: str


class RequestDataScheme(BaseModel):
    frameworks: str = None
    tags: str = None
    categories: int = None



