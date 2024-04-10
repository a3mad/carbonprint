from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    electricity = Column(Float, index=True)
    natural_gas = Column(Float, index=True)
    fuel = Column(Float, index=True)
    waste = Column(Float, index=True)
    recycled_percent = Column(Float, index=True)
    business_travels = Column(Float, index=True)
    fuel_efficency = Column(Float, index=True)
    energy_usage = Column(Float, index=True)
    waste_generation = Column(Float, index=True)
    business_travel = Column(Float, index=True)
    total = Column(Float, index=True)
