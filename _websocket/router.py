from utils.ConnectionManager import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter
from auth.models import User
from control.models import Control
from car.models import UserCar
from sqlmodel import select
from auth.utils import validate_jwt
from fastapi import Depends
from fastapi import HTTPException
from db import get_session
import json

router = APIRouter()
manager = ConnectionManager() 


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    session: AsyncSession = Depends(get_session)
):
    print("-----------------------------")
    token = websocket.headers.get("Authorization")
    token = websocket.query_params.get("token") if token is None else token
    if not token:
        print("Missing token, closing connection")
        await websocket.close()
        return

    device_type = websocket.headers.get("device_type") 
    device_type = websocket.query_params.get("device_type") if device_type is None else device_type
    print(f"Device type: {device_type}")
    print(device_type == 'user')
    if device_type == "car":
        # key = websocket.headers.get("Authorization")
        result = await session.execute(select(UserCar).where(UserCar.key == token))
        user_car = result.scalar_one_or_none()
        if user_car is None:
            await websocket.close()
            return
        result = await session.execute(select(User).where(User.id == user_car.user_id))
        username = result.scalar_one().username
        
    elif device_type == "user":
        try:
            username = validate_jwt(token)
        except HTTPException as e:
            print("manga")
            print(e.detail)
            await websocket.close()
            return
    else:
        print("invalid device_type ")
        await websocket.close()
        return

    await manager.connect(websocket, username)
    try:
        while True:
            print(device_type)
            obj = await websocket.receive_text()
            # check if the obj can be converted to a json object
            try:
                obj = json.loads(obj)
            except json.JSONDecodeError as e:
                print("Received data is not a json object: ", e)
                continue

            print(f"Received obj: {obj}")
            if manager.checkIfOtherSideIsConnected(websocket, username):
                if device_type == 'car':
                    print("sending to the user that the message is received. ")
                    success = await manager.send_to_car(json.dumps(obj), username)
                    print(f"Message sent: {success}")
                elif device_type == 'user':
                    await handle_car_message(session, obj, username)
            else:
                if device_type == 'user':
                    print("sending to the user that the car is not connected. ")
                    message = {"type": "notification", "message": "Car is not connected"}
                    message = json.dumps(message)
                    await manager.send_to_user(message, username)

            print("Connection manager:")
            print(manager)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")


async def handle_car_message(session: AsyncSession, data: dict, username: str):
    try:
        type = data["type"]
        if type == "basicControl":
            print("Handling basic control")
            await handle_car_basic_control(data, username)
        elif type == "switchMode":
            print("Handling switch mode")
            await handle_car_switch_mode(data, username)
        elif type == "customControl":
            print("Handling calling custom control")
            await handle_car_custom_control(session, data, username)
        else:
            raise Exception("Invalid message type")
    except Exception as e:
        print(f"Error handling car message: {e}")


async def handle_car_switch_mode(data: dict, username: str):
    mode = data["mode"]
    allowed_modes = ["follow-mode", "safe-mode", "free-mode"]
    if mode not in allowed_modes:
        print(f"{mode} is not a valid mode, only {allowed_modes} are allowed")
        return
    print(f"Switching mode to {mode}")
    message = {"type": "switchMode", "mode": mode}
    message = json.dumps(message)
    print(f"Sending to {username} message: {message}")
    is_sent = await manager.send_to_car(message, username)
    print(f"Message sent: {is_sent}")


async def handle_car_basic_control(data: dict, username: str):
    # make sure that the data is right
    if data["type"] == "basicControl":
        if data.get("action") is not None and isinstance(data.get("action"), list):
            if data["action"][0] == "set-speed":
                if data["action"][1] >= 50 and data["action"][1] <= 255:
                    # redirect the message to the car
                    await manager.send_to_car(json.dumps(data), username)
                else:
                    print("Invalid speed")

            elif data["action"][0] == "set-direction":
                allowed_directions = ["forward", "backward", "left", "right", "stop"]
                if data["action"][1] in allowed_directions:
                    # redirect the message to the car
                    await manager.send_to_car(json.dumps(data), username)
            else:
                print("Invalid action")
        else:
            print("Invalid action")
    else:
        print("Invalid type")

async def handle_car_custom_control(session: AsyncSession, data, username):
    id = data.get("id")
    if id is None:
        print("Missing id")
        return

    result = await session.execute(select(Control).where(Control.custom_control_id == id))
    controls = result.scalars().all()
    actions = []
    mapper = {
        1: "forward",
        2: "backward",
        3: "left",
        4: "right",
        5: "stop",
    }
    for control in controls:
        bs_id = control.basic_control_id
        if bs_id in range(1, 6):
            if bs_id == 5:
                actions.append(["set-direction", "stop"])
            else:
                actions.append(["set-direction", mapper[control.basic_control_id], control.value])
        elif bs_id == 6:
            actions.append(["set-speed", control.value])
        
    print(f"Sending to car: {actions}")
    message = {"type": "customControl", "actions": actions}
    message = json.dumps(message)
    is_sent = await manager.send_to_car(message, username)
    print(f"Message sent: {is_sent}")
