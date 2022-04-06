from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database_ import Base


class Plants(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(String(128), nullable=False)
    category = Column(String(32), nullable=False)
    vase = Column(String(32))
    water_sprinklers_id = Column(Integer, ForeignKey('water_sprinklers.id'))
    water_sprinklers = relationship("WaterSprinkler", backref="plants", passive_deletes=True)

    def __init__(self, name, description, category, vase, water_sprinklers_id):
        self.name = name
        self.description = description
        self.category = category
        self.vase = vase
        self.water_sprinklers_id = water_sprinklers_id
