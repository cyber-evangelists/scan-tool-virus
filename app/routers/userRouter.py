from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from app.models.db_models.user import User
from app.models.request_models.signUpRequest import CreateUserRequest

router = APIRouter()

@router.post("/signup", tags=["USER ROUTES"])
async def signup_user(user: CreateUserRequest):
    return user