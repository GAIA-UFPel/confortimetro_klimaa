from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.controllers import AuthController, DeviceController, LocationController, MetricController, MetricTypeController
from app.database import get_session
from app.models import User
from app.request_forms import LoginRequest, RegisterRequest, DeviceStoreRequest, LocationStoreRequest, MetricStoreRequest, MetricTypeStoreRequest
from app.utils.auth import auth

router = APIRouter()

@router.post("/login")
async def login(req: LoginRequest,
                session: AsyncSession = Depends(get_session)):
    return await AuthController.login(
        req,
        session
    )
    
@router.post("/register")
async def register(req: RegisterRequest,
                session: AsyncSession = Depends(get_session)):
    return await AuthController.register(
        req,
        session
    )

@router.get("/confirm-email")
async def confirm_email(token: str = Query(None),
                        user: User = Depends(auth.get_current_user), 
                        session: AsyncSession = Depends(get_session)):
    return AuthController.confirm_email(
        token,
        user,
        session
    )

@router.get("/device")
async def index_device(user: User = Depends(auth.get_current_user),
                      session: AsyncSession = Depends(get_session)):
    return DeviceController.index(
        session
    )

@router.get("/device/{id}")
async def show_device(id: int,
                      user: User = Depends(auth.get_current_user), 
                      session: AsyncSession = Depends(get_session)):
    return DeviceController.show(
        id,
        session
    )
    
@router.post("/device")
async def store_device(req: DeviceStoreRequest,
                       user: User = Depends(auth.requires('admin')()),
                       session: AsyncSession = Depends(get_session)):
    return DeviceController.store(
        req,
        session
    )

@router.get("/location")
async def index_location(user: User = Depends(auth.get_current_user),
                        session: AsyncSession = Depends(get_session)):
    return LocationController.index(
        session
    )

@router.get("/location/{id}")
async def get_location_by_id(id: int,
                             user: User = Depends(auth.requires('admin')()),
                             session: AsyncSession = Depends(get_session)):
    return LocationController.show(
        id,
        session
    )

@router.post("/location")
async def store_location(req: LocationStoreRequest,
                         user: User = Depends(auth.requires('admin')()),
                         session: AsyncSession = Depends(get_session)):
    return LocationController.store(
        req,
        session
    )

@router.get("/metric/{id}")
async def index_metric(id: int,
                       user: User = Depends(auth.get_current_user),
                       session: AsyncSession = Depends(get_session)):
    return MetricController.show(
        id,
        session
    )

@router.post("/metric")
async def store_metric(req: MetricStoreRequest,
                       user: User = Depends(auth.requires('admin')()),
                       session: AsyncSession = Depends(get_session)):
    return MetricController.store(
        req,
        session
    )

@router.get("/metric-type")
def index_metric_type(user: User = Depends(auth.get_current_user), 
                      session: AsyncSession = Depends(get_session)):
    return MetricTypeController.index(
        session
    )

@router.post("/metric-type")
def store_metric_types(req: MetricTypeStoreRequest, 
                       user: User = Depends(auth.get_current_user), 
                       session: AsyncSession = Depends(get_session)):
    return MetricTypeController.store(
        req,
        session
    )

@router.get("/metric-type/{id}")
def show_metric_type(id: int,
                     user: User = Depends(auth.get_current_user), 
                     session: AsyncSession = Depends(get_session)):
    return MetricTypeController.show(
        id, 
        session
    )