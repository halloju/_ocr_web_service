from app.database import Base, schema_name
from sqlalchemy import Column, DateTime, String, Integer, Float
from sqlalchemy.sql import func


class OCRResults(Base):
    __tablename__ = "ocr_results"
    __table_args__ = {"schema": schema_name, "extend_existing": True}
    image_cv_id = Column(String, primary_key=True, nullable=False)
    tag = Column(String, nullable=True)
    det_model = Column(String, nullable=True)
    rec_model = Column(String, nullable=True)
    text = Column(String, nullable=True)
    det_prob = Column(Float, nullable=True)
    rec_prob = Column(Float, nullable=True)
    x_1 = Column(Integer, nullable=False)
    y_1 = Column(Integer, nullable=False)
    x_2 = Column(Integer, nullable=False)
    y_2 = Column(Integer, nullable=False)
    x_3 = Column(Integer, nullable=False)
    y_3 = Column(Integer, nullable=False)
    x_4 = Column(Integer, nullable=False)
    y_4 = Column(Integer, nullable=False)
    etl_dt = Column(DateTime(timezone=True), onupdate=func.now())
