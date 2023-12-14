import os
import secrets
import jwt
from datetime import datetime, timedelta

from .schemes import UserInfo, User, UserInDB, UserLogin
from database import get_async_session
from models.models import userdata

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from .utls import generate_token, verify_token

register_router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'])


@register_router.post('/register')
async def register(user: User, session: AsyncSession = Depends(get_async_session)):
    if user.password1 == user.password2:
        if not select(userdata).where(userdata.c.username == user.username).exists:
            raise HTTPException(status_code=400, detail='Username already in use!')
        if not select(userdata).where(userdata.c.email == user.email).exists:
            raise HTTPException(status_code=400, detail='Email already in use!')
        password = pwd_context.hash(user.password1)
        user_in_db = UserInDB(**dict(user), password=password,created_at=datetime.utcnow() )
        query = insert(userdata).values(**dict(user_in_db))
        await session.execute(query)
        await session.commit()
        user_info = UserInfo(**dict(user))
        return dict(user_info)


@register_router.post('/login')
async def login(user:UserLogin,session:AsyncSession = Depends(get_async_session)):
    query = select(userdata).where(userdata.c.username == user.username)
    user__data = await session.execute(query)
    try:
        user_data = user__data.one()
    except NoResultFound:
        raise HTTPException(status_code=404,detail='Username or password is incorrect!')
    if pwd_context.verify(user.password,user_data.password):
        token = generate_token(user_data.id)
        return token
    else:
        raise HTTPException(status_code=404,detail='Username or password is incorrect!')

@register_router.get('/user-info',response_model=UserInfo)
async def user_info(
        token:dict = Depends(verify_token),
        session:AsyncSession = Depends(get_async_session)
):
    if token is None:
        raise HTTPException(status_code=401,detail='Not registered!')
    user_id = token.get('user_id')
    query = select(userdata).where(userdata.c.id == user_id)
    user__data = await  session.execute(query)
    try:
        user_data = user__data.one()
        return user_data
    except NoResultFound:
        raise HTTPException(status_code=404,detail='User is not found!')








