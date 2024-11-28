from sqlmodel import Field, SQLModel, Column


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=30, nullable=False, unique=True)
    first_name: str = Field(max_length=30, nullable=False)
    last_name: str = Field(max_length=30, nullable=False)
    password: str = Field(nullable=False)
    car_speed: int = Column(default=50)
    def __str__(self):
        return self.username
