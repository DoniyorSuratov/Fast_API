import os
from datetime import timedelta
from typing import List
from sqlalchemy import select, insert, update,delete
from .schemes import (MainProductsScheme,
                      AboutProductsScheme,
                      CartAddProductsScheme,
                      CartShowProductsScheme)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_async_session
from models.models import product, cart
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import func
from auth.utls import verify_token
from fastapi.responses import FileResponse

market_router = APIRouter()

@market_router.get('/all-products', response_model=List[MainProductsScheme])    #gets all products list
async def get_top_freebies(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product)
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/freebies', response_model=List[MainProductsScheme])    #gets all freebies produstss list
async def get_freebies(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product).where(product.c.status == 'Free')
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/premium-templates', response_model=List[MainProductsScheme])   #gets all premium products list
async def get_premium_templates(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product).where(product.c.status != 'Free')
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/recent-released', response_model=List[MainProductsScheme])     #gets all last 3 days added products list
async def get_recent_released(session: AsyncSession =Depends(get_async_session)):
    try:
        query = select(product).where(product.c.created_at >= func.current_timestamp() - timedelta(days=3))
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/more-about-theme', response_model=AboutProductsScheme)   #gets only one product which was selected by product_id
async def get_more_about_theme(product_id: int,session: AsyncSession = Depends(get_async_session)):
    query = select(product).where(product.c.id == product_id)
    query_data = await session.execute(query)
    product_data = query_data.one()
    return product_data


@market_router.post('/cart/')              # Add to cart
async def add_to_cart(
                    product_id: CartAddProductsScheme,
                    token: dict = Depends(verify_token),
                    session: AsyncSession = Depends(get_async_session)
                ):

    # Retrieve product information based on the product_id
    product_query = select(product).where(product.c.id == product_id.product_id)
    product_result = await session.execute(product_query)
    product_info = product_result.one()

    user_id = token.get('user_id')
    product_id_in_cart = select(cart).where((cart.c.product_id == product_id.product_id) & (cart.c.user_id == user_id))
    product_id_in_cart_ = await session.execute(product_id_in_cart)
    product_id_in_cart_result = product_id_in_cart_.all()

    if product_id_in_cart_result: # check is product already exists in cart
        return HTTPException(status_code=400, detail='Product already exists')
    else:
        # Add the product information to the cart table
        query = insert(cart).values(
            user_id=token.get('user_id'),
            product_id = product_info.product_id
        )
        await session.execute(query)
        await session.commit()
        return {'success': True, 'message': 'Your template added to cart'}


@market_router.get('/cart/', response_model=List[CartShowProductsScheme]) # show products in cart
async def show_cart(
                    session: AsyncSession = Depends(get_async_session),
                    token: dict =  Depends(verify_token)):
    if token is None:
        raise HTTPException(status_code=403, detail='Forbidden')

    query = select(cart).where(cart.c.cart_owner_user_id == token.get('user_id'))
    data = await session.execute(query)
    get_data = data.all()


    product_list =[]
    for pro in get_data:
        query2 = select(product).where(product.c.id == pro.product_id)
        product_detail = await session.execute(query2)
        product__detail = product_detail.one()._asdict()
        shopping_dict = {
            'owner_id': pro.cart_owner_user_id,
            'product_info': product__detail,
            'license': pro.license
        }
        product_list.append(shopping_dict)
    return product_list


@market_router.delete('/cart/') # delete product from cart
async def delete_cart(product_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      token: dict =  Depends(verify_token)):

    user_id_ = token.get('user_id')
    query = delete(cart).where((cart.c.product_id == product_id) & (cart.c.cart_owner_user_id == user_id_))
    await session.execute(query)
    await session.commit()
    return {'success': True, 'message': 'Your cart has been deleted'}


@market_router.get('/download-template/{hashcode}') #download templates
async def download_template(
        hashcode: str,
        session: AsyncSession = Depends(get_async_session)
):
    if hashcode is None:
        raise HTTPException(status_code=400, detail='Invalid hashcode')

    query = select(product).where(product.c.hash == hashcode)
    template__data = await session.execute(query)
    file_data = template__data.one()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_url = os.path.join(f'{BASE_DIR}/media/{file_data.filepath}')
    file_name = file_data.filepath.split('/')[-1]
    print(file_url)
    return FileResponse(path=file_url,media_type="application/octet-stream", filename=file_name)

