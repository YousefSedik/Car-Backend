from sqlmodel import SQLModel, Field


class UserCar(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    key: str = Field(nullable=False)
    
    def __str__(self):
        return "Car key: " + self.key