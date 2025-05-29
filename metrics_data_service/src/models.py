from sqlalchemy import Column, Integer, String, DateTime, Float
# from sqlalchemy.ext.declarative import declarative_base # Replaced by Base from database
from datetime import datetime
from .database import Base # Import Base from database.py

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    source = Column(String, nullable=True)  # e.g., sensor_id, service_name

    # TODO: Add any other relevant fields for your metrics
    # e.g., tags (JSON or a separate table), units, etc.

# TODO: Define other models if needed
# e.g., User model for authentication, etc.
