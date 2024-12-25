from fastapi import FastAPI
from auth.router import router as auth_router
from _websocket.router import router as web_socket_router
from control.router import router as control_router 

app = FastAPI()

app.include_router(auth_router, tags=["Authentication"])
app.include_router(web_socket_router)
app.include_router(control_router, tags=["Control"])
