from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update

from auth.auth import register_router
from database import get_async_session
from models.models import blog
from schemes import Blog, BlogPost

app = FastAPI()
router = APIRouter()


@router.post('/blogs')
async def create_blog(new_blog: BlogPost, session: AsyncSession = Depends(get_async_session)):
    query = insert(blog).values(**dict(new_blog))
    await session.execute(query)
    await session.commit()
    return {'success': True, 'message': 'Successfully posted'}


@router.get('/blogs', response_model=List[Blog])
async def blog_list(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(blog)
        blog_data = await session.execute(query)
        blog_data = blog_data.all()
        return blog_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')


@router.get('/blogs/{blog_id}', response_model=Blog)
async def blog_detail(blog_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(blog).where(blog.c.id == blog_id)
    blog_data = await session.execute(query)
    blog_data = blog_data.one()
    view_count = blog_data.view_count
    query2 = update(blog).where(blog.c.id == blog_id).values(view_count=view_count + 1)
    await session.execute(query2)
    await session.commit()
    return blog_data


app.include_router(router)
app.include_router(register_router)
