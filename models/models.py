from datetime import datetime
import enum


from sqlalchemy import (Column,
                        Table,
                        Integer,
                        String,
                        Text,
                        Boolean,
                        MetaData,
                        TIMESTAMP,
                        ForeignKey,
                        Boolean,
                        Enum,
                        )
from datetime import datetime
metadata = MetaData()

userdata = Table(
    'userdata',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String, nullable=True),
    Column('last_name', String, nullable=True),
    Column('email', String),
    Column('phone', String),
    Column('username', String),
    Column('password', String),
    Column('created_at', TIMESTAMP, default=datetime.utcnow())

)

# class CategoryEnum(enum.Enum):
#     adminDashboard = 'Admin & Dashboard'
#     bootstrap5 = 'Bootstrap5'
#     ecomerce = 'eComerce'
#     tailwindCSS = 'Tailwind CSS'
#     landingPages = 'Landing Pages'
#     bussinesCorporate = 'Business & Corporate'
#     portfolio = 'Portfolio'
#     educational = 'Educational'

product = Table(
    'product',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('image', String),
    Column('description', Text),
    # Column('category', Enum(CategoryEnum)),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('category_id', ForeignKey('category.id')),
    Column('user_id', ForeignKey('userdata.id')),
    Column('status', String, default='Free'),
    Column('version', String),
    Column('updated_at', TIMESTAMP),
    Column('frameworks', String),
    Column('compatible_with', String),
    Column('tags', String),
    Column('filepath', String),
    Column('hash', String, unique=True)


)


category = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String)
)


cart = Table(
    'cart',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('cart_owner_user_id', ForeignKey('userdata.id')),
    Column('product_id', ForeignKey('product.id')),
    Column('license', String, default='Standart')

)

subscriber = Table(
    'subscriber',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String, unique=True),
)

blog = Table(
    'blog',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(length=150), nullable=False),
    Column('description', Text),
    Column('created_at', TIMESTAMP, default=datetime.utcnow()),
    Column('blog_owner', ForeignKey('userdata.id')),
)



