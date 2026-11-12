
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class ExploredDisease(Base):
    __tablename__ = "explored_diseases"

    id = Column(Integer, primary_key=True)
    disease_id = Column(
        Integer,
        ForeignKey("diseases.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    explored_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
