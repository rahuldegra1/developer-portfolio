from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, unique=True, index=True)
    gender = Column(String)
    senior_citizen = Column(Boolean, default=False)
    subscription = relationship("Subscription", back_populates="user", uselist=False)


class Subscription(Base):
    __tablename__ = "subscriptions"
    sub_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    tenure_months = Column(Integer)
    monthly_charges = Column(Float)
    total_charges = Column(Float)
    churn = Column(Boolean, default=False)
    user = relationship("User", back_populates="subscription")
