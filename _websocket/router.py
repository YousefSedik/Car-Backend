from utils.ConnectionManager import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter
from auth.models import User
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
    token = websocket.query_params.get("token", "")
    if not token:
        print("Missing token, closing connection")
        await websocket.close()
        return

    try:
        username = validate_jwt(token)
        # set the username to the websocket query params
    except HTTPException as e:
        print(e.detail)
        await websocket.close()
        return

    await manager.connect(websocket, username)
    try:
        while True:
            obj = await websocket.receive_text()
            # check if the obj can be converted to a json object
            try:
                obj = json.loads(obj)
            except json.JSONDecodeError as e:
                print("Received data is not a json object: ", e)
                continue

            print(f"Received obj: {obj}")
            device_type = websocket.query_params.get("device_type", "")
            data = obj["data"]
            if device_type == "":
                print("Device type is empty")
                manager.disconnect(websocket)
            if manager.checkIfOtherSideIsConnected(websocket, username):
                if device_type == 'car':
                    await handle_user_message (
                        obj["type"], data, username
                    )
                else:
                    await handle_car_message(obj["type"], data, username)
            else:
                print("other side is not connected to the server.")

            print("Connection manager:")
            print(manager)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")


async def handle_car_message(type: str, data: dict, username: str):
    try:

        if type == "basicControl":
            print("Handling basic control")
            await handle_car_basic_control(data, username)
        elif type == "switchMode":
            print("Handling switch mode")
            await handle_car_switch_mode(data, username)
        else:
            raise Exception("Invalid message type")
    except Exception as e:
        print(f"Error handling car message: {e}")

async def handle_car_switch_mode(data: dict, username: str):
    mode = data["mode"]
    allowed_modes = ["follow-mode", "safe-mode"]
    if mode not in allowed_modes:
        print(f"{mode} is not a valid mode, only {allowed_modes} are allowed")
        return
    print(f"Switching mode to {mode}")
    message = {"type": "switchMode", "mode": mode}
    message = json.dumps(message)
    print(f"Sending to {username} message: {message}")
    is_sent = await manager.send_to_car(message, username)
    print(f"Message sent: {is_sent}")

async def handle_user_message(type: str, data: dict, username: str):
    try:
        pass
    except Exception as e:
        print(f"Error handling user message: {e}")


async def handle_car_basic_control(data: dict, username: str):
    action_obj = data["action"]
    if type(action_obj) is dict:
        print("Action is a dict")
        # then, the action could be [Go Forward, Go Backward, Change Speed]
        print(action_obj.keys())
        action = list(action_obj.keys())[0]
        if action == "Change Speed":
            await handle_car_basic_control_change_speed(action_obj, username)
        elif action in ["Go Forward", "Go Backward"]:
            await handle_user_basic_control_start_direction(action_obj, action, username)
        else:
            print("Invalid action")
    elif type(action_obj) is str:
        print("Action is a string")
        if action_obj == "Stop":
            await handle_user_basic_control_stop(username)


async def handle_car_basic_control_change_speed(action_obj: dict, username):
    speed = action_obj["Change Speed"]
    if speed <= 100 and speed >= 1:
        print("Speed is in the range")
    else:
        print("Speed is not in the range")
        return 
    print("Changing speed")
    message = {"type": "basicControl", "action": "Change Speed", "speed": speed}
    print(f"Sending to {username} message: {message}")
    message = json.dumps(message)
    is_sent = await manager.send_to_car(message, username)
    print(f"Message sent: {is_sent}")

async def handle_user_basic_control_start_direction(action_obj: dict, action: int, username: str):
    '''
    Go Forward, Go Backward
    '''
    print(action)
    to_infinity = action_obj[action].get("ToInfinity", True)
    if to_infinity:
        message = {"type": "basicControl", "action": action, "ToInfinity": to_infinity}
    else:
        forSeconds = action_obj[action].get("ForSeconds", 1)
        message = {"type": "basicControl", "action": action, "ToInfinity": to_infinity, "forSeconds": forSeconds}
    print(f"Sending to {username} message: {message}")

    message = json.dumps(message)
    is_sent = await manager.send_to_car(message, username)
    print(f"Message sent: {is_sent}")

async def handle_user_basic_control_stop(username):
    print("Stopping the car")
    message = {"type": "basicControl", "action": "Stop"}
    message = json.dumps(message)
    print(f"Sending to {username} message: {message}")
    is_sent = await manager.send_to_car(message, username)
    print(f"Message sent: {is_sent}")
