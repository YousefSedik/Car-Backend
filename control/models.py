from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class BasicControl(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Integer primary key
    name: str = Field(max_length=255)  # String with a maximum length constraint


class CustomControl(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Integer primary key
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(max_length=255)  # String with a maximum length constraint
    description: str = Field(
        max_length=1024, nullable=True, default=None
    )  # String with a larger max length for descriptions
    # controls: List['Control'] = Relationship(back_populates="custom_control")


class Control(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Integer primary key
    custom_control_id: int = Field(
        foreign_key="customcontrol.id"
    )  # Foreign key reference to CustomControl
    basic_control_id: int = Field(
        foreign_key="basiccontrol.id"
    )  # Foreign key reference to BasicControl
    value: Optional[int] = Field(default=None, ge=0, nullable=True)  # Optional non-negative float for distance

