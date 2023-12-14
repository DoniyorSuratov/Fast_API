from datetime import datetime

from pydantic import BaseModel



class User(BaseModel):
    first_name:str
    last_name:str
    email:str
    phone:str
    username:str
    password1:str
    password2:str


class UserInDB(BaseModel):
    first_name:str
    last_name:str
    email:str
    phone:str
    username:str
    password:str
    created_at:datetime


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    username: str




class UserLogin(BaseModel):
    username:str
    password:str

