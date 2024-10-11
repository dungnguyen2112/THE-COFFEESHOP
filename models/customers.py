from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    address = Column(String(255), default='')
    loyalty_id = Column(Integer, ForeignKey('customer_loyalty.loyalty_id'), nullable=True)
    total_spent = Column(Float, default=0.0)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)

    role = relationship("Role", back_populates="customers")
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    loyalty = relationship("CustomerLoyalty", back_populates="customers")
