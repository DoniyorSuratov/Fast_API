from datetime import datetime
from sqlalchemy import (Column,
                        Table,
                        Integer,
                        String,
                        Text,
                        Boolean,
                        MetaData,
                        TIMESTAMP,
                        Boolean,
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




blog = Table(
    'blog',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(length=150), nullable=False),
    Column('description', Text),
    Column('created_date', TIMESTAMP, default=datetime.utcnow),
    Column('is_active', Boolean, default=True),
    Column('view_count', Integer, default=0)
)