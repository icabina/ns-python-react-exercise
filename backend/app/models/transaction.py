from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, index=True) # e.g., 'credit', 'debit'
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    category_rel = relationship("Category", back_populates="transactions", lazy="selectin")
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, index=True) # Mocked authentication

