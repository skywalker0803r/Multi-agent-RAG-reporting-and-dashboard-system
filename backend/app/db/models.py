from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.database import Base

class ReturnWarrantyData(Base):
    __tablename__ = "return_warranty_data"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    customer_id = Column(String, index=True)
    return_date = Column(DateTime, default=func.now())
    warranty_claim_date = Column(DateTime, nullable=True)
    reason = Column(Text)
    status = Column(String)
    price = Column(Float)
    notes = Column(Text, nullable=True)

    # You can add more fields relevant to your retail data

    def __repr__(self):
        return f"<ReturnWarrantyData(id={self.id}, product_id='{self.product_id}')>"