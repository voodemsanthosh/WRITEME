from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating a new metric
class MetricCreate(BaseModel):
    name: str
    value: float
    source: Optional[str] = None
    timestamp: Optional[datetime] = None

# Schema for reading/returning a metric
class Metric(MetricCreate):
    id: int
    timestamp: datetime # Make timestamp non-optional for display

    class Config:
        orm_mode = True # Allows Pydantic to work with ORM objects

# TODO: Define other schemas as needed
# e.g., for updating metrics, user authentication, etc.
