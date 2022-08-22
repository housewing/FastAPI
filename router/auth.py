from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from model.auth import get_user, create_user, validate_user
from model.jwt_token import create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

@router.post('/register')
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user:
        create_user(form_data)
        return {'message': 'create user finish'}
    return {'message': 'create user fail'}

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = validate_user(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
