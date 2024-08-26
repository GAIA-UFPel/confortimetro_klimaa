from fastapi import Response
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Location
from app.request_forms import LocationStoreRequest

class LocationController:
    @classmethod
    async def index(cls,
                    session: AsyncSession):
        locations = await session.exec(select(Location))

        return locations
    
    @classmethod
    async def show(cls,
                   id: int,
                   session: AsyncSession):
        location = (await session.exec(select(Location).where(Location.id == id))).first()

        return location

    @classmethod
    async def store(cls,
                    req: LocationStoreRequest,
                    session: AsyncSession):
        location = Location(
            campus = req.campus,
            building = req.building,
            room = req.room
        )

        session.add(location)
        await session.commit()

        return Response(status_code=200)