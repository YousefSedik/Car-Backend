# create websocket router

from fastapi.routing import APIRouter
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from utils.ConnectionManager import ConnectionManager
import json


router = APIRouter()

manager = ConnectionManager() 


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):

    await manager.connect(websocket)
    try:
        while True:
            obj = await websocket.receive_text()
            obj = json.loads(obj)
            print("-----------------------------")
            print(f"Received obj: {obj}")
            device_type = websocket.query_params.get("device_type", "")
            obj_type = obj["type"]
            data = obj["data"]
            if manager.checkIfOtherSideIsConnected(websocket):
                print("Sending to user")
                successed = await manager.send_to_user(
                    data, websocket.query_params.get("username", "")
                )
                if not successed:
                    print("user is not connected")
            else:
                print("other side is not connected to the server.")

            print("Connection manager:")
            print(manager)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
