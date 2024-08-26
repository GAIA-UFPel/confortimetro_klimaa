from datetime import datetime
from typing import Annotated
from fastapi import Query   
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: Annotated[EmailStr, Query(max_length=60)]
    password: Annotated[str, Query(min_length=8)]

class RegisterRequest(BaseModel):
    username: Annotated[str, Query(max_length=50)]
    email: Annotated[EmailStr, Query(max_length=60)]
    password: Annotated[str, Query(min_length=8)]
    is_admin: Annotated[bool, Query(default=False)]
    is_active: Annotated[bool, Query(default=False)]
    has_write_access: Annotated[bool, Query(default=False)]

class DeviceStoreRequest(BaseModel):
    serial_number: str
    model: str
    location_id: int

class LocationStoreRequest(BaseModel):
    campus: str
    building: str
    room: str

class MetricStoreRequest(BaseModel):
    date_time: datetime
    device_id: int
    location_id: int
    metric_type_id: int
    value: float

class MetricTypeStoreRequest(BaseModel):
    name: str
    description: str