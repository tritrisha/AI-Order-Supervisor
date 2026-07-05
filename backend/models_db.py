from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Run(Base):
    __tablename__ = "runs"

    run_id = Column(String, primary_key=True)
    status = Column(String, default="RUNNING")
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship(
        "Message",
        back_populates="run",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)

    run_id = Column(
        String,
        ForeignKey("runs.run_id"),
        nullable=False,
    )

    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    run = relationship("Run", back_populates="messages")


class MemorySummary(Base):
    __tablename__ = "memory_summary"

    run_id = Column(String, primary_key=True)

    summary = Column(Text)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )