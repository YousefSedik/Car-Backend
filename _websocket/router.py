from utils.ConnectionManager import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter
from auth.models import User
from sqlmodel import select
from fastapi import Depends
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
    username = websocket.query_params.get("username", "")
    user_exists = await session.execute(select(User).where(User.username == username))
    user_exists = user_exists.scalars().first()
    if not user_exists:
        print("User does not exist, closing connection")    
        await websocket.close()
        return
    await manager.connect(websocket)
    try:
        while True:
            obj = await websocket.receive_text()
            # check if the obj can be converted to a json object
            try:
                obj = json.loads(obj)
            except json.JSONDecodeError:
                print("Received data is not a json object")
                continue

            print(f"Received obj: {obj}")
            device_type = websocket.query_params.get("device_type", "")
            username = websocket.query_params.get("username", "")
            data = obj["data"]

            if manager.checkIfOtherSideIsConnected(websocket):
                if device_type == 'car':
                    return await handle_user_message (
                        obj["type"], data, username
                    )
                else:
                    return await handle_car_message(obj["type"], data, username)
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
        else:
            raise Exception("Invalid message type")
    except Exception as e:
        print(f"Error handling car message: {e}")


async def handle_user_message(type: str, data: dict, username: str):
    try:
        pass
    except Exception as e:
        print(f"Error handling user message: {e}")


async def handle_car_basic_control(data: dict, username: str):
    action_obj = data["action"]
    if type(action_obj) is dict:
        print("Action is a dict")
        # then, the action could be Go Forward, Go Backward, Change Speed
        print(action_obj)
        print(action_obj.keys())
        action = list(action_obj.keys())[0]
        if action == "Change Speed":
            print("Changing speed")
            speed = action_obj["Change Speed"]
            message = {"type": "basicControl", "action": "Change Speed", "NewSpeed": speed}
            print(f"Sending to {username} message: {message}")
            message = json.dumps(message)
            await manager.send_to_car(message, username)
        elif action in ["Go Forward", "Go Backward"]:
            print(action)
            to_infinity = action_obj[action].get("ToInfinity", True)
            if to_infinity:
                message = {"type": "basicControl", "action": action, "ToInfinity": to_infinity}
            else:
                forSeconds = action_obj["Go Forward"].get("ForSeconds", 1)
                message = {"type": "basicControl", "action": action, "ToInfinity": to_infinity, "forSeconds": forSeconds}
            print(f"Sending to {username} message: {message}")

            message = json.dumps(message)
            await manager.send_to_car(message, username)
        else:
            print("Invalid action")
    elif type(action) is str:
        print("Action is a string")
        if action == "Stop":
            print("Stopping the car")
            message = {"type": "basicControl", "action": "Stop"}
            message = json.dumps(message)
            await manager.send_to_car(message, username)
