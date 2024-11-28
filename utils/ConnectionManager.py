from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # Key: WebSocket object, Value: (username, device_type)
        self.active_connections: dict[WebSocket, tuple[str, str]] = {}

    async def connect(self, websocket: WebSocket):
        """
        Accepts the WebSocket connection, retrieves user details from query parameters,
        and adds the connection to the active connections dictionary.
        """
        await websocket.accept()

        try:
            params = websocket.query_params
            username = params.get(
                "username", ""
            ).lower()
            device_type = params.get(
                "device_type", ""
            ).lower()

            # Validate device_type
            if device_type not in ["user", "car"]:
                await websocket.close(code=1003)  # 1003: Unsupported Data
                raise ValueError(
                    f"Invalid device_type: {device_type}. Expected 'user' or 'car'."
                )

            # Add connection to the dictionary
            self.active_connections[websocket] = (username, device_type)
            print(f"New connection: username={username}, device_type={device_type}")
        except Exception as e:
            print(f"Error connecting WebSocket: {e}")
            await websocket.close()

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections dictionary.
        """
        if websocket in self.active_connections:
            del self.active_connections[websocket]
            print(f"Disconnected: {websocket}")

    async def send_to_user(self, message: str, user_id: int):
        """
        Sends a message to the specified user by user_id.
        """
        for ws, (username, device_type) in self.active_connections.items():
            try:
                if username == user_id and device_type == "user":
                    await ws.send_text(message)
                    return True
            except Exception as e:
                print(f"Error sending message: {e}")
        
        return False

    async def send_to_car(self, message: str, car_id: int):
        """
        Sends a message to the specified car by car_id.
        """
        for ws, (username, device_type) in self.active_connections.items():
            try:
                if username == car_id and device_type == "car":
                    await ws.send_text(message)
                    return True
            except Exception as e:
                print(f"Error sending message: {e}")
        
        return False
    def checkIfOtherSideIsConnected(self, websocket: WebSocket):
        """
        Checks if the other side (user or car) is connected to the server.
        """
        username = websocket.query_params.get("username", "")
        device_type = websocket.query_params.get("device_type", "")
        for ws, (username, device_type) in self.active_connections.items():
            if username == username and device_type != device_type:
                return True
        return False
    
    def __str__(self) -> str:
        result = ""
        for websocket, (username, device_type) in self.active_connections.items():
            result += f"username: {username} ({device_type})\n"
        return result