from fastapi import HTTPException, Response
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import MetricType
from app.request_forms import MetricTypeStoreRequest

class MetricTypeController:
    @classmethod
    async def index(cls,
              session: AsyncSession):
        metric_types = await session.exec(select(MetricType))

        return metric_types
    
    @classmethod
    async def show(cls,
             id: int,
             session: AsyncSession):
        metric_type = (await session.exec(select(MetricType).where(MetricType.id == id))).first()
        if not metric_type:
            raise HTTPException(status_code=404, detail="Metric type not found")

        return metric_type
    
    @classmethod
    async def store(cls, 
              req: MetricTypeStoreRequest,
              session: AsyncSession):
        metric_type = MetricType(
            name = req.name,
            description = req.description
        )

        session.add(metric_type)
        await session.commit()

        return Response(status_code=200)