
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from app.models.db_models.user import User
from app.models.request_models.signUpRequest import CreateUserRequest

from fastapi import APIRouter, HTTPException

from app.models.db_models.user import User
from app.models.request_models.signUpRequest import CreateUserRequest
from app.models.request_models.loginRequest import LoginUserRequest
from app.auth.auth_handler import signJWT
from app.services.logs import logger
from app.services.utils import hash_password, verify_password


router = APIRouter()

@router.post("/signup", tags=["USER ROUTES"])
async def signup_user(user: CreateUserRequest):

    return user

    user.password = hash_password(user.password)
    check_user = await User.find_one({"username": user.username})
    if check_user:
        raise HTTPException(400, detail="User already exists")
    
    user_dict = user.dict()
    new_user = User(**user_dict)

    inserted_result = await User.create(new_user)
    logger.info(f"User [{user.username}] inserted in database")
    return {"inserted":True} if inserted_result else None

@router.post("/login", tags=["USER ROUTES"])
async def login_user(user: LoginUserRequest):
    fetched_user = await User.find_one({"username": user.username})
    if fetched_user is None:
        raise HTTPException(status_code=401, detail="Sorry, please sign up first")
    elif fetched_user == False:
        raise HTTPException(
            status_code=500, detail="Server was unable to perform the query"
        )
    if not verify_password(user.password, fetched_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    token = signJWT(user.username)
    return token

