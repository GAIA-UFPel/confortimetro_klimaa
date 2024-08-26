from fastapi import Response, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Device, Location
from app.request_forms import DeviceStoreRequest

class DeviceController:
    @classmethod
    async def index(cls,
                    session: AsyncSession):
        devices = await session.exec(select(Device))

        return devices
    
    @classmethod
    async def show(cls,
                   id: int,
                   session: AsyncSession):
        device = (await session.exec(select(Device).where(Device.id == id))).first()
    
        return device

    @classmethod
    async def store(cls,
              req: DeviceStoreRequest,
              session: AsyncSession):
        location = (await session.exec(select(Location).where(Location.id == req.location_id))).first()
        if not location:
            raise HTTPException(status_code=400, detail="Location not found, please create it first.")

        device = Device(
            serial_number = req.serial_number,
            model = req.model,
            id_location = location.id
        )

        session.add(device)
        await session.commit()

        return Response(status_code=200)
