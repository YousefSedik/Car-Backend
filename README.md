# FastAPI Backend for ESP32 Car Remote

## Overview

This project provides a FastAPI-based backend API that acts as the communication bridge between an ESP32-powered car and a frontend application. The backend enables users to remotely control the car's movements and retrieve telemetry data in real-time.

## Features

- WebSocket Support: Real-time communication with the frontend and ESP32 hardware.

- API Endpoints: RESTful endpoints for controlling and monitoring the car.

- Authentication: Secure access to the API for authorized users using JWT and key-based authentication for cars.

- Data Logging: Stores telemetry and user actions for future analysis.

## Prerequisites

- Python 3.10+

- FastAPI

- PostgreSQL (or any database of choice, with configuration)

## Installation

1. Clone the repository
```
git clone https://github.com/YousefSedik/Car-Backend
cd Car-Backend
```
2. Create a virtual environment and activate it
```python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Configure environment variables

Create a .env file in the project root and define the following variables:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your_secret_key
DEBUG=True
```
5. Apply migrations
```
alembic upgrade head
```
## Usage

Start the server
```
uvicorn main:app --reload
```
The API will be accessible at http://127.0.0.1:8000.

## API Endpoints

REST Endpoints

`POST` `/register`: Register a new user.

Payload example:
```
{
  "username": "string",
  "password1": "string",
  "password2": "string",
  "first_name": "string",
  "last_name": "string"
}
```

`POST` `/token`: Obtain a JWT token for authentication.

`GET` `/users/me` : Retrieve the current user's information (authentication required).

`GET` `/basic-control`: Retrieve basic control commands for the car.

`GET` `/custom-control`: Get a list of predefined custom control actions.

`POST` `/custom-control`: Create a custom control action.

Example: Define an action to move forward for 10 cm, turn right, and then change the speed to 200.

`GET` `/custom-control/{id}`: Retrieve a custom control action by ID.

`GET` `/key`: Retrieve all car keys for the authenticated user.

`POST` `/key`: Generate a new key for a car.

`DELETE` `/key`: Delete an existing car key.

## WebSocket Endpoint

`/ws`: Establish a WebSocket connection for real-time car control.

The frontend or ESP32 can send directional commands such as "go forward" or "move right" to control the car.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

