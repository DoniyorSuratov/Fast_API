from datetime import timedelta
from typing import List
from sqlalchemy import select
from fastapi import APIRouter
from .schemes import MainProductsScheme
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_async_session
from models.models import product
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import func
market_router = APIRouter()

@market_router.get('/all-products', response_model=List[MainProductsScheme])  #gets all products list
async def get_top_freebies(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product)
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/freebies', response_model=List[MainProductsScheme]) #gets all freebies produstss list
async def get_freebies(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product).where(product.c.status == 'Free')
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/premium-templates', response_model=List[MainProductsScheme]) #gets all premium products list
async def get_premium_templates(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product).where(product.c.status != 'Free')
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/recent-released', response_model=List[MainProductsScheme])  #gets all last 3days added products list
async def get_recent_released(session: AsyncSession =Depends(get_async_session)):
    try:
        query = select(product).where(product.c.created_at >= func.current_timestamp() - timedelta(days=3))
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')