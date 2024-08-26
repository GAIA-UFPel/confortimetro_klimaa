from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, String, CheckConstraint
from fastapi_user_auth.auth.models import BaseUser

class Device(SQLModel, table=True):
    __tablename__ = 'devices'

    id: int = Field(primary_key=True)
    serial_number: str = Field(String(40), index=True)
    model: str = Field(String(30))
    location_id: int = Field(foreign_key='locations.id')

    location: 'Location' = Relationship(back_populates='locations')

class Location(SQLModel, table=True):
    __tablename__ = 'locations'

    id: int = Field(primary_key=True)
    campus: str
    building: str
    room: str

    devices: List['Device'] = Relationship(back_populates='devices')

class Metric(SQLModel, table=True):
    __tablename__ = 'metrics'

    id: int = Field(primary_key=True)
    datetime: datetime
    device_id: int = Field(foreign_key='devices.id')
    location_id: int = Field(foreign_key='locations.id')
    metric_type_id: int = Field(foreign_key='metric_types.id')
    value: float

    device: 'Device' = Relationship(back_populates='devices')
    location: 'Location' = Relationship(back_populates='locations')
    metric_type: 'MetricType' = Relationship(back_populates='metric_types')

class MetricType(SQLModel, table=True):
    __tablename__ = 'metric_types'

    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    description: Optional[str]

class User(BaseUser):
    group: str = Field(sa_column_args=[CheckConstraint("group IN ('student', 'professor', 'external community')")])