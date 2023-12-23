from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from fastapi.staticfiles import StaticFiles
from auth.auth import register_router
from database import get_async_session
from market.market import market_router
from schemes import Blog, BlogPost

app = FastAPI()
router = APIRouter()


app.include_router(register_router)
app.include_router(market_router)
app.mount('/media', StaticFiles(directory='media'), 'templates')