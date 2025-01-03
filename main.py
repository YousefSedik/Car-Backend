from fastapi import FastAPI
from auth.router import router as auth_router
from _websocket.router import router as web_socket_router
from fastapi.middleware.cors import CORSMiddleware
from control.router import router as control_router
from car.router import router as car_router

app = FastAPI()

app.include_router(auth_router, tags=["Authentication"])
app.include_router(web_socket_router)
app.include_router(control_router, tags=["Control"])
app.include_router(car_router, tags=["Car"])


origins = [
    "http://192.168.1.13:3000",
    "http://localhost:3000",
    "https://car-controller-neon.vercel.app/",
    "https://car-controller-neon.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
