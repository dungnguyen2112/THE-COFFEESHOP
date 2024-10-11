from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class CustomerLoyalty(Base):
    __tablename__ = 'customer_loyalty'
    loyalty_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String(50), nullable=False)
    loyalty_points = Column(Integer, nullable=False)
    loyalty_description = Column(String(255), nullable=True)

    customers = relationship("Customer", back_populates="loyalty")
