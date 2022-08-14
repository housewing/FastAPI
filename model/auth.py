from config.connect_string import connect_list
from config.sql import user_sql
from model.database import DBconnect
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union
import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
current_milli_time = lambda: int(round(time.time() * 1000))

class User(BaseModel):
    id: Union[str, None] = None
    username: Union[str, None] = None
    password: Union[str, None] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str)->User:
    db_connect = DBconnect(connect_list.get('518'), 'WLS')
    desc, data = db_connect.query(user_sql.get('get_user').format(username))
    for row in data:
        return User(
            id=row.id,
            username=row.username,
            password=row.password
        )
    return None

def create_user(form_data):
    data = [[current_milli_time(), form_data.username, get_password_hash(form_data.password)]]
    db_connect = DBconnect(connect_list.get('518'), 'WLS')
    db_connect.insert(user_sql.get('create_user'), data)

def validate_user(form_data):
    user = get_user(form_data.username)
    if not user:
        return False

    if not verify_password(form_data.password, user.password):
        return False
    return user