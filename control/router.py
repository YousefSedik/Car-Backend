from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, responses
from auth.models import User
from sqlmodel import select
from fastapi import Depends
from fastapi import HTTPException
from db import get_session
from sqlalchemy.orm import selectinload
from control.models import CustomControl, Control, BasicControl
from control.schemas import CreateControlSchema
from auth.utils import get_current_user

router = APIRouter()


@router.get("/basic-control")
async def get_basic_control(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(BasicControl))
    controls = result.scalars().all()
    return controls 


@router.post("/custom-control")
async def create_custom_control(
    custom_control_schema: CreateControlSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    custom_control = CustomControl(
        name=custom_control_schema.name,
        description=custom_control_schema.description,
        user_id=current_user.id,
    )

    session.add(custom_control)
    await session.commit()
    session.refresh(custom_control)

    for control in custom_control_schema.basic_controls:
        control_new_obj = Control(
            custom_control_id=custom_control.id,
            basic_control_id=control.get("basicControl_id"),
        )

        if control.get("basicControl_id") in range(1, 5):
            print("control is from 1 to 4")
            control_new_obj.value = control.get("distance")
        elif control.get("basicControl_id") == 5:
            print("control is stop")
        elif control.get("basicControl_id") == 6:
            print("control is change speed")
            control_new_obj.value = control.get("new-speed")

        session.add(control_new_obj)

    await session.commit()
    return responses.Response(custom_control.dict(), 201)


@router.get("/custom-control/{id}")
async def get_custom_control_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    custom_control = await session.get(CustomControl, id)
    
    if custom_control is None:
        raise HTTPException(status_code=404, detail="Control not found")
    if custom_control.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return custom_control

@router.get("/custom-control")
async def get_custom_controls(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)):
    # get all custom control and control objects associated with it
    result = await session.execute(
        select(CustomControl)
        .options(selectinload(CustomControl.controls))  # Eager load controls
        .where(CustomControl.user_id == current_user.id)
    )
    custom_controls = result.scalars().all()
    return custom_controls


