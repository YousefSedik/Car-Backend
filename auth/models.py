from sqlmodel import Field, SQLModel, Column


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=30, nullable=False, unique=True)
    first_name: str = Field(max_length=30, nullable=False)
    last_name: str = Field(max_length=30, nullable=False)
    password: str = Field(nullable=False)
    def __str__(self):
        return self.username


class UserCar(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    key: str = Field(nullable=False) 