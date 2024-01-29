import os

from datetime import timedelta, datetime
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SMTP_CODE = os.getenv('SMTP_CODE')


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from typing import List

import json
from sqlalchemy import select, insert, update, delete
from .schemes import (MainProductsScheme,
                      AboutProductsScheme,
                      CartAddProductsScheme,
                      CartShowProductsScheme, BlogScheme, BlogGETScheme, )
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models.models import product, cart, subscriber, blog, userdata
from fastapi import Depends, APIRouter, HTTPException

import secrets
from datetime import timedelta
from typing import List
from sqlalchemy import select, insert, update, delete
from .schemes import (
    MainProductsScheme,
    AboutProductsScheme,
    CartAddProductsScheme,
    CartShowProductsScheme, AddProductScheme, RequestDataScheme
)
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models.models import product, cart
from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import func
from auth.utls import verify_token
from fastapi.responses import FileResponse
import aiofiles

market_router = APIRouter()



@market_router.get('/all-products', response_model=List[MainProductsScheme])    #gets all products list

@market_router.get('/all-products', response_model=List[MainProductsScheme])  # gets all products list

async def get_top_freebies(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product)
        query_data = await session.execute(query)
        products = query_data.all()
        print(products)
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/freebies', response_model=List[MainProductsScheme])  # gets all freebies produstss list
async def get_freebies(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product).where(product.c.status == 'Free')
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/premium-templates', response_model=List[MainProductsScheme])  # gets all premium products list
async def get_premium_templates(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product).where(product.c.status != 'Free')
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/recent-released',
                   response_model=List[MainProductsScheme])  # gets all last 3 days added products list
async def get_recent_released(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(product).where(product.c.created_at >= func.current_timestamp() - timedelta(days=3))
        query_data = await session.execute(query)
        products = query_data.all()
        return products
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Product not found')


@market_router.get('/more-about-theme',
                   response_model=AboutProductsScheme)  # gets only one product which was selected by product_id
async def get_more_about_theme(product_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(product).where(product.c.id == product_id)
    query_data = await session.execute(query)
    product_data = query_data.one()
    return product_data


@market_router.post('/cart/')  # Add to cart
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
    product_id_in_cart = select(cart).where(
        (cart.c.product_id == product_id.product_id) & (cart.c.cart_owner_user_id == user_id))
    product_id_in_cart_ = await session.execute(product_id_in_cart)
    product_id_in_cart_result = product_id_in_cart_.all()

    if product_id_in_cart_result:  # check is product already exists in cart
        return HTTPException(status_code=400, detail='Product already exists')
    else:
        # Add the product information to the cart table
        query = insert(cart).values(
            cart_owner_user_id=token.get('user_id'),
            product_id=product_info.product_id
        )
        await session.execute(query)
        await session.commit()
        return {'success': True, 'message': 'Your template added to cart'}


@market_router.get('/cart/', response_model=List[CartShowProductsScheme])  # show products in cart
async def show_cart(

                    session: AsyncSession = Depends(get_async_session),
                    token: dict = Depends(verify_token)):
        session: AsyncSession = Depends(get_async_session),
        token: dict = Depends(verify_token)):
    if token is None:
        raise HTTPException(status_code=403, detail='Forbidden')

    query = select(cart).where(cart.c.cart_owner_user_id == token.get('user_id'))
    data = await session.execute(query)
    get_data = data.all()

    product_list =[]
    product_list = []
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


@market_router.delete('/cart/')  # delete product from cart
async def delete_cart(product_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      token: dict = Depends(verify_token)):

    user_id_ = token.get('user_id')
    query = delete(cart).where((cart.c.product_id == product_id) & (cart.c.cart_owner_user_id == user_id_))
    await session.execute(query)
    await session.commit()
    return {'success': True, 'message': 'Your cart has been deleted'}


@market_router.get('/download-template/{hashcode}')  # download templates
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
    return FileResponse(path=file_url, media_type="application/octet-stream", filename=file_name)


@market_router.post('/add-template')
async def add_template(
        file: UploadFile = File(...),
        image: UploadFile = File(None),
        product_: AddProductScheme = Depends(),
        session: AsyncSession = Depends(get_async_session),
        token: dict = Depends(verify_token)
):
    user_id = token.get('user_id')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_file1 = os.path.join(f'{BASE_DIR}/media/templates/{file.filename}')
    file_loc = f'templates/{file.filename}'

    # save file of template (required)
    if file.filename.endswith(('tar', 'rar', 'zip')):
        async with aiofiles.open(out_file1, mode='wb') as f1:
            content = await file.read()
            await f1.write(content)
            await f1.close()
    else:
        return {'succes': 'False', 'message': 'Not valid format of file'}
        # save photo of template (not required)
    if image.filename.endswith(('.jpg', '.jpeg', '.png')):
        out_file2 = os.path.join(f'{BASE_DIR}/media/images/{image.filename}')
        image_loc = f'images/{image.filename}'
    else:
        return {'succes': 'False', 'message': 'Not valid format of photo'}

    async with aiofiles.open(out_file2, mode='wb') as f1:
        content = await image.read()
        await f1.write(content)
    hashcode = secrets.token_hex(32)

    query = insert(product).values(
        user_id=user_id,
        frameworks=product_.frameworks,
        compatible_with=product_.compatible_with,
        tags=product_.tags,
        name=product_.name,
        description=product_.description,
        category_id=product_.category_id,
        version=product_.version,
        filepath=file_loc,
        image=image_loc,
        hash=hashcode
    )
    await session.execute(query)
    await session.commit()
    return {'success': 'ok'}



@market_router.get('/filter', response_model=List[MainProductsScheme])
async def product_filter(
        data: RequestDataScheme = Depends(),
        session: AsyncSession = Depends(get_async_session)
):

    query = select(product)

    if data.tags:
        query = query.where(product.c.tags.contains(data.tags))

    if data.frameworks:
        query = query.where(product.c.frameworks.contains(data.frameworks))

    if data.categories is not None:
        query = query.where(product.c.category_id.contains(data.categories))

    data = await session.execute(query)
    template_data = data.all()
    return template_data


@market_router.post('/subscribe/')
async def subscribe(
        email: str,
        session: AsyncSession = Depends(get_async_session)
                    ):
    query = select(subscriber).where(subscriber.c.email == email)
    query1 = await session.execute(query)
    q_data = query1.all()
    if q_data:
        return {'success': False, 'message': 'This email is already subscribed !!!'}
    else:
        query_email = insert(subscriber).values(email=email)
        await session.execute(query_email)
        await session.commit()
        return {'success': True, 'Response': 'Subscribe DONE'}


@market_router.get("/blogs", response_model=List[BlogGETScheme])
async def get_blogs(
        session: AsyncSession = Depends(get_async_session),

):
    query_blog = select(blog)
    blog_data = await session.execute(query_blog)
    blog__data = blog_data.all()
    lis = []
    for blog_ in blog__data:
        print(blog_[4])
        query_user = select(userdata).where(userdata.c.id == blog_[4])
        owner = await session.execute(query_user)
        owner_ = owner.first()
        lis.append({
            'id': blog_[0],
            'title': blog_[1],
            'description': blog_[2],
            'created_at': blog_[3],
            'blog_owner': owner_
        })
    await session.commit()
    return lis


@market_router.post('/blog-create/')
async def create_blog(
        new_blog_data: BlogScheme,
        session: AsyncSession = Depends(get_async_session),
        token: dict = Depends(verify_token)
):
    user_id = token.get('user_id')
    query_user = select('*').select_from(userdata).where(userdata.c.id == user_id)
    user_ = await session.execute(query_user)
    user = user_.first()
    query_blog = insert(blog).values(
        title=new_blog_data.title,
        description=new_blog_data.description,
        blog_owner=user.id,
        created_at=datetime.utcnow()
    )
    await session.execute(query_blog)
    query_email = select(subscriber)
    email_data = await session.execute(query_email)
    emails = email_data.all()
    await session.commit()
    for email in emails:
        sender_email = SENDER_EMAIL
        receiver_email = email[1]
        subject = 'New blog'
        message = {
            'title': new_blog_data.title,
            'owner': f'{user.first_name} {user.last_name}',
            'link': f'https//:127.0.0.1:8000/market/blogs',
        }
        message_string = json.dumps(message)
        # SMTP server configuration for gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = SENDER_EMAIL
        smtp_password = SMTP_CODE

        # Create a multipart message and set headers
        email_message = MIMEMultipart()
        email_message['From'] = sender_email
        email_message['To'] = receiver_email
        email_message['Subject'] = subject

        email_message.attach(MIMEText(message_string, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            server.send_message(email_message)

        print('Success')

    await session.commit()
    return {'success': True, 'message': 'Blog created successfully'}
