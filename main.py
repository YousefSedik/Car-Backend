from fastapi import FastAPI, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

app = FastAPI()

@app.get("/")
async def ping():
    return {"message": "pong"}
