from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
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

# switch to mode

# @app.get("/")
# async def get_joystick():
#     return RedirectResponse(url="/ws")
    # return HTMLResponse(content=open("templates/joystick.html", encoding="utf8").read())

@app.get("/basic-control")
async def get_basic_control(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(BasicControl.name))
    result = result.scalars().all()
    return result
