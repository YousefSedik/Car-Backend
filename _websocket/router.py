from utils.ConnectionManager import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter
from auth.models import User
from control.models import Control, CustomControl
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
            allowed_directions = ["forward", "backward", "left", "right", ]
            if data["action"][0] in allowed_directions and data["action"][1] in range(50, 256):
                await manager.send_to_car(
                    json.dumps(
                        {
                            "type": "basicControl",
                            "action": [data["action"][0], data["action"][1]],
                        }
                    ),
                    username,
                )
            elif data["action"][0] == "stop":
                await manager.send_to_car(
                    json.dumps(
                        {
                            "type": "basicControl",
                            "action": [data["action"][0]],
                        }
                    ),
                    username,
                )
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
    print(f"Handling custom control with id: {id}")
    result = await session.execute(select(CustomControl).where(CustomControl.id == id))
    control = result.scalars().first()
    if control is None:
        await manager.send_to_user(json.dumps({"notification": "Custom control not found"}), username)
        return
    print(control)
    description = json.loads(control.description)
    print(f"Sending to car: {description}")
    message = {"type": "customControl", "actions": description}
    message = json.dumps(message)
    is_sent = await manager.send_to_car(message, username)
    print(f"Message sent: {is_sent}")
