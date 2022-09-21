from app.database import Base, schema_name
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

class LoginHist(Base):
    __tablename__ = "login_hist"
    __table_args__ = {"schema": schema_name, "extend_existing": True}
    id = Column(Integer, primary_key=True)
    account = Column(String)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
