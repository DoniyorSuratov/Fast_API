from fastapi import FastAPI
from pydantic import BaseModel, Field
app = FastAPI()

fake_users = [
    {'id': 1, 'role': 'admin', 'name':'Bob'},
    {'id': 2, 'role': 'trader', 'name':'Jack'},
    {'id': 3, 'role': 'developer', 'name':'Sam'},
]

class MessageScheame(BaseModel):
    message: str


class UserScheame(BaseModel):
    id: int = Field(gt=0)
    role: str = Field(max_length=10)
    name: str


@app.get('/hello/{name}', response_model=MessageScheame)
def hello(name):
    return {'message': f'Hello world! {name}'}


@app.get('/users')
def users_list():
    return fake_users


@app.get('/users/{user_id}')
def user_detail(user_id: int):
    user = list(filter(lambda x : x.get('id') == user_id, fake_users))[0]
    return user


@app.post('/users')
def add_user(user: UserScheame):
    fake_users.append(dict(user))
    return user