from fastapi.routing import APIRouter
from auth.schemas import LoginForm, SignUpForm
from dotenv import load_dotenv
from auth.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from auth.utils import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_user,
    get_current_user,
)
from fastapi import Response
from db import get_session
from auth.models import User, UserCar
from datetime import timedelta, datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
load_dotenv()

router = APIRouter()


@router.post("/register")
async def register(
    SignUpForm: SignUpForm, session: AsyncSession = Depends(get_session)
):
    await create_user(session, SignUpForm)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/token", response_model=Token)
async def login(
    form_data: LoginForm, session=Depends(get_session)
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expire
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/users/me")
async def read_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return {
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
    }

@router.post("/key")
async def generate_key(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    key = str(uuid4()).replace("-", "")
    user_car = UserCar(user_id=current_user.id, key=key)
    session.add(user_car)
    await session.commit()
    return {
        "key": key
    }
    
@router.get("/key")
async def get_all_cars_for_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(UserCar.key).where(UserCar.user_id == current_user.id))
    cars = result.scalars().all()
    return cars