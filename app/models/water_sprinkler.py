from datetime import date

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from app.db.database_ import Base


class WaterSprinkler(Base):
    __tablename__ = "water_sprinklers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    is_active = Column(Boolean, default=True)
    description = Column(String(128), nullable=False)

    def __init__(self, name, description, is_active):
        self.name = name
        self.description = description
        self.is_active = is_active


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_start = Column(Date, default=date.today())
    hour_watering = Column(Integer, nullable=False)
    minutes_watering = Column(Integer, nullable=False)
    pressure = Column(Integer, nullable=False)
    water_flow = Column(Integer, nullable=False)
    opening_time = Column(Integer(), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    water_sprinklers_id = Column(Integer, ForeignKey('water_sprinklers.id'))
    water_sprinklers = relationship("WaterSprinkler", backref="settings", passive_deletes=True)

    def __init__(self,
                 date_start, hour_watering, minutes_watering,
                 pressure, water_flow, opening_time, is_active,
                 water_sprinklers_id):
        self.date_start = date_start
        self.hour_watering = hour_watering
        self.minutes_watering = minutes_watering
        self.pressure = pressure
        self.water_flow = water_flow
        self.opening_time = opening_time
        self.is_active = is_active
        self.water_sprinklers_id = water_sprinklers_id
