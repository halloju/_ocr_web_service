from app.database import Base, schema_name
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": schema_name, "extend_existing": True}
    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    enable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
