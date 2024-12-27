from pydantic import BaseModel


class DeleteCarKey(BaseModel):
    car_key: str

