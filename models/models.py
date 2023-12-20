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
                        DateTime)
metadata=MetaData()

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
    Column('created_at', TIMESTAMP, default=datetime.utcnow()
           )

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
    Column('description', Text),
    # Column('category', Enum(CategoryEnum)),
    Column('created_at', TIMESTAMP, default=datetime.utcnow()),
    Column('category_id', ForeignKey('category.id')),
    Column('user_id', ForeignKey('userdata.id')),
    Column('status', String, default='Free'),
    Column('version', String),
    Column('updated_at', TIMESTAMP, default=datetime),
    Column('frameworks', String),
    Column('compatible_with', String),
    Column('tags', String)

)


category = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String)
)