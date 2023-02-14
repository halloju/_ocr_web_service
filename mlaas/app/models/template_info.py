from app.database import Base, schema_name
from sqlalchemy import Column, DateTime, String, ARRAY, JSON, Boolean
from sqlalchemy.sql import func

class TemplateInfo(Base):
    __tablename__ = "template_info"
    __table_args__ = {"schema": schema_name, "extend_existing": True}
    template_id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, nullable=False)
    template_name = Column(String, nullable=False)
    bbox = Column(ARRAY(JSON(String)), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_public = Column(Boolean, nullable=False)
    is_no_ttl = Column(Boolean, nullable=False)
