from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # Key: WebSocket object, Value: (username, device_type)
        self.active_connections: dict[WebSocket, tuple[str, str]] = {}
        # Key: username, Value: list of device_type
        self.active_connections_usernames: dict[str, list[str]] = {}

    async def connect(self, websocket: WebSocket, username: str):
        """
        Accepts the WebSocket connection, retrieves user details from query parameters,
        and adds the connection to the active connections dictionary.
        """

        await websocket.accept()

        try:
            params = websocket.query_params
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
            if username not in self.active_connections_usernames:
                self.active_connections_usernames[username] = [device_type]
            else:
                self.active_connections_usernames[username].append(device_type)
            print(f"New connection: username={username}, device_type={device_type}")
        except Exception as e:
            print(f"Error connecting WebSocket: {e}")
            await websocket.close()

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections dictionary.
        """

        if websocket in self.active_connections:
            username, device_type = self.active_connections[websocket]
            del self.active_connections[websocket]
            self.active_connections_usernames[username].remove(device_type)
            print(f"Disconnected: {websocket}")

    async def send_to_user(self, message: str, username: str):
        """
        Sends a message to the specified user by username.
        """
        for ws, (user_username, device_type) in self.active_connections.items():
            try:
                if user_username == username and device_type == "user":
                    await ws.send_text(message)
                    return True
            except Exception as e:
                print(f"Error sending message: {e}")

        return False

    async def send_to_car(self, message: str, username: int):
        """
        Sends a message to the specified car by car_id.
        """
        for ws, (car_username, device_type) in self.active_connections.items():
            try:
                if car_username == username and device_type == "car":
                    await ws.send_text(message)
                    return True
            except Exception as e:
                print(f"Error sending message: {e}")
        return False
    
    def checkIfOtherSideIsConnected(self, websocket: WebSocket, username: str):
        """
        Checks if the other side (user or car) is connected to the server.
        """
        # username = websocket.query_params.get("username", "")
        device_type = websocket.query_params.get("device_type", "")

        if (device_type == "car" and "user" in self.active_connections_usernames.get(username)):
            return True
        if device_type == "user" and "car" in self.active_connections_usernames.get(username):
            return True
        return False

    def __str__(self) -> str:
        result = ""
        for websocket, (username, device_type) in self.active_connections.items():
            result += f"username: {username} ({device_type})\n"
        return result
