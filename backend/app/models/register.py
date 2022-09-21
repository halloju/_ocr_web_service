from app.database import Base, schema_name
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Account(Base):
    __tablename__ = "account"
    __table_args__ = {"schema": schema_name, "extend_existing": True}
    account = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    birthday = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
