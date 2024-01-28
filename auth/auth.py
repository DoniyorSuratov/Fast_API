
from datetime import datetime, timedelta

from .schemes import UserInfo, User, UserInDB, UserLogin
from database import get_async_session
from models.models import userdata

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import Depends, APIRouter, HTTPException
from passlib.context import CryptContext

from .utls import generate_token, verify_token

register_router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'])


@register_router.post('/login')
async def login(user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    query = select(userdata).where(userdata.c.username == user.username)
    user__data = await session.execute(query)
    try:
        user_data = user__data.first()
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Username or password is incorrect!')
    if pwd_context.verify(user.password, user_data.password):
        token = generate_token(user_data.id)
        return token
    else:
        raise HTTPException(status_code=404,detail='Username or password is incorrect!')


@register_router.post('/register')
async def register(user: User, session: AsyncSession = Depends(get_async_session)):
    if user.password1 != user.password2:
        raise HTTPException(status_code=400, detail="Password don't match!")

    try:
        user_name = select(userdata).where(userdata.c.username == user.username)
        user_name_result = await session.execute(user_name)
        user_ = user_name_result.scalar()
        if user_:
            raise HTTPException(status_code=400,detail="Username already exists!")
    except NoResultFound:
        pass

    try:
            email = select(userdata).where(userdata.c.email == user.email)
            email_result = await session.execute(email)
            email_ = email_result.scalar()
            if email_:
                raise HTTPException(status_code=400, detail="Email already exists!")
    except NoResultFound:
            pass

    password = pwd_context.hash(user.password1)
    user_in_db = UserInDB(**dict(user), password=password, created_at=datetime.now())
    user_in_db_dict = user_in_db.dict()
    query = insert(userdata).values(user_in_db_dict)
    await session.execute(query)
    await session.commit()
    user_info = UserInfo(**dict(user))
    return dict(user_info)


@register_router.get('/user-info', response_model=UserInfo)
async def user_info(
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    if token is None:
        raise HTTPException(status_code=401, detail='Not registered!')
    user_id = token.get('user_id')
    query = select(userdata).where(userdata.c.id == user_id)
    user__data = await session.execute(query)
    try:
        user_data = user__data.first()
        return user_data
    except NoResultFound:
        raise HTTPException(status_code=404, detail='User is not found!')







