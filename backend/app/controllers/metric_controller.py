from fastapi import HTTPException, Response
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Metric, Location, Device, MetricType
from app.request_forms import MetricStoreRequest

class MetricController:
    @classmethod
    async def index(cls,
                    session: AsyncSession):
        metrics = await session.exec(select(Metric))

        return metrics
    
    @classmethod
    async def show(cls,
                   id: int,
                   session: AsyncSession):
        metrics = (await session.exec(select(Metric).where(Metric.id == id))).first()

        return metrics

    @classmethod
    async def store(cls,
                    req: MetricStoreRequest,
                    session: AsyncSession):
        metric = Metric(
            date_time = req.date_time,
            device_id= req.device_id,
            location_id = req.location_id,
            metric_type_id = req.metric_type_id,
            value = req.value
        )

        session.add(metric)
        await session.commit()

        return Response(status_code=200)