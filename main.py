from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, Response

app = FastAPI()


@app.get("/")
async def get_joystick():

    print(open("templates/joystick.html", encoding="utf8").read())
    return HTMLResponse(content=open("templates/joystick.html", encoding="utf8").read())


# Manage connected clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            # Broadcast the message to all connected clients
            await manager.broadcast(f"Action {data} received on the server!")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
