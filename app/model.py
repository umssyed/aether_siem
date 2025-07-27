from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class HistoricalUsage(Base):
    __tablename__ = "historical_usage"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    hostname = Column(String(100))
    process_name = Column(String(255))
    cpu = Column(Float)
    mem = Column(Float)
    reason = Column(String)
