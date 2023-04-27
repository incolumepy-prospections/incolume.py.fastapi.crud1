import datetime as dt
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional


user_db = {
    'ada': {'username': 'ada', 'date_joined': '2021-12-01', 'state': 'São Paulo', 'age': 28},
    'ana': {'username': 'ana', 'date_joined': '2021-12-02', 'state': 'Distrito Federal', 'age': 19},
    'aca': {'username': 'acã', 'date_joined': '2021-12-03', 'state': 'Acre', 'age': 52}
}


class User(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    date_joined: dt.datetime = Field(default_factory=dt.datetime.utcnow)
    location: Optional[str] = None
    age: int = Field(None, gt=5, lt=130)  # ge: greater than or equal, le


class UserUpdate(User):
    date_joined: Optional[dt.datetime] = None
    age: int = Field(None, gt=5, lt=200)


def ensure_username_in_db(username: str):
    if username not in user_db:
        raise HTTPException(status_code=404, detail=f'Username {username} not found')


app = FastAPI()


@app.get('/users/{username}')
def get_users_path(username: str):
    ensure_username_in_db(username)
    return user_db[username]


@app.get('/users')
def get_users_query(offset: int = 0, limit: int = 20):
    user_list = list(user_db.values())
    return user_list[offset:limit]


@app.post('/users')
def create_user(user: User):
    username = user.username
    if username in user_db:
        # status.HTTP_409_CONFLICT
        raise HTTPException(status_code=409, detail=f'Cannot create user. Username {username} already exists')
    user_db[username] = user.dict()
    return {'message': f'Successfully created user: {username}'}


@app.delete('/users/{username}')
def delete_user(username: str):
    ensure_username_in_db(username)
    del user_db[username]
    return {'message': f'Successfully deleted user {username}'}


@app.put('/users')
def update_user(user: User):
    username = user.username
    ensure_username_in_db(username)
    user_db[username] = user.dict()
    return {'message': f'Successfully updated user {username}'}


@app.patch('/users')
def update_user_partial(user: UserUpdate):
    username = user.username
    ensure_username_in_db(username)
    user_db[username].update(user.dict(exclude_unset=True))
    return {'message': f'Successfully updated user {username}'}