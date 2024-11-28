from sqlmodel import Field, SQLModel


class BasicControl(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    

# 1, go forward
# 2, go backward
# 3, turn left
# 4, turn right
# 5, stop
# 6, speed up
# alembic revision --autogenerate -m "Initial Migration"