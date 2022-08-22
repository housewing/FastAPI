from fastapi import APIRouter, Depends, HTTPException, status
from model.jwt_token import get_current_user
from model.auth import User

router = APIRouter()

@router.get("/user/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
