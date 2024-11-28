from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from auth.router import router as auth_router
from _websocket.router import router as web_socket_router
from fastapi import Depends
from db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from _websocket.models import BasicControl
from sqlmodel import select
app = FastAPI()
app.include_router(auth_router)
app.include_router(web_socket_router)



@app.get("/")
async def get_joystick():
    return HTMLResponse(content=open("templates/joystick.html", encoding="utf8").read())

@app.get("/basic-control")
async def get_basic_control(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(BasicControl.name))
    result = result.scalars().all()
    return result



@app.get("/create-control")
async def get_crate_control(
    session: AsyncSession = Depends(get_session)
):
    # b1 = BasicControl(name="Go Forward")
    # b2 = BasicControl(name="Go Backward")
    # b3 = BasicControl(name="Go Left")
    # b4 = BasicControl(name="Go Right")
    # b5 = BasicControl(name="Stop")
    # b6 = BasicControl(name="Change Speed")
    # session.add(b1)
    # session.add(b2)
    # session.add(b3)
    # session.add(b4)
    # session.add(b5)
    # session.add(b6)
    from sqlalchemy.sql import text
    await session.execute(text("DELETE FROM basiccontrol"))
    await session.commit()