from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'user_id': self.user_id,
        }


class MenuItem(Base):
    __tablename__ = 'menuitem'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    price = Column(String(8))
    item_type = Column(String(80))
    car_id = Column(Integer, ForeignKey('car.id'))
    description = Column(String(250))
    car = relationship(Car)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'item_type': self.item_type,
            'car_id': self.car_id,
            'user_id': self.user_id,
        }


''' insert at end of file '''

engine = create_engine('sqlite:///carmenuuser.db')
Base.metadata.create_all(engine)
