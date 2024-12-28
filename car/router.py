from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from db import get_session
from auth.models import User
from car.models import UserCar
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils import get_current_user
from car.schemas import DeleteCarKey
router = APIRouter()

@router.post("/key")
async def generate_key(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    key = str(uuid4()).replace("-", "")
    user_car = UserCar(user_id=current_user.id, key=key)
    session.add(user_car)
    await session.commit()
    return {"key": key}


@router.get("/key")
async def get_all_cars_for_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(UserCar.key).where(UserCar.user_id == current_user.id)
    )
    cars = result.scalars().all()
    return cars


@router.delete("/key")
async def delete_key(
    car_key_form: DeleteCarKey,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(UserCar).where(UserCar.key == car_key_form.car_key)
    )
    user_car = result.scalar_one_or_none()
    if user_car.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to delete this key"
        )
    if user_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    await session.delete(user_car)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
