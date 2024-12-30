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
import json

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
    # ensure that the custom control name is unique
    custom_control_schema.name = custom_control_schema.name.lower().strip()
    result = await session.execute(
        select(CustomControl).where(CustomControl.name == custom_control_schema.name)
    )
    existing_control = result.scalars().first()
    if existing_control:
        raise HTTPException(
            status_code=400, detail="Custom control name already exists"
        )
    custom_control = CustomControl(
        name=custom_control_schema.name,
        description=json.dumps(custom_control_schema.description),
        user_id=current_user.id,
    )

    session.add(custom_control)
    await session.commit()
    await session.refresh(custom_control)

    return responses.Response(status_code=201)


@router.get("/custom-control")
async def get_custom_controls(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Get all custom controls with associated control objects
    result = await session.execute(
        select(CustomControl.id, CustomControl.name, CustomControl.description).where(
            CustomControl.user_id == current_user.id
        )
    )
    custom_controls = [{"id": row[0], "name": row[1], "description": json.loads(row[2]) if row[2] else None} for row in result.all()]
    return custom_controls


@router.delete("/custom-control/{control_id}")
async def delete_custom_control(
    control_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Control).where(Control.custom_control_id == control_id)
    )
    controls = result.scalars().all()
    for control in controls:
        await session.delete(control)
    await session.commit()
    
    result = await session.execute(
        select(CustomControl).where(CustomControl.id == control_id)
    )
    
    custom_control = result.scalars().first()
    if not custom_control:
        raise HTTPException(status_code=404, detail="Custom control not found")
    if custom_control.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await session.delete(custom_control)
    await session.commit()
    return responses.Response(status_code=204)
