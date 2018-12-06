from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy import create_engine

Base = declarative_base()


class Hospital(Base):
    __tablename__ = 'hospital'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), primary_key=True)
    phone = Column(String(30), nullable=False)
    location = Column(String(30), nullable=False)

    @validates('name')
    def update_name(self, key, value):
        self.bloodbank.name = value
        return value


class BloodBank(Base):
    __tablename__ = 'bloodbank'

    name = Column(String(50), primary_key=True)
    location = Column(String(30), nullable=False)
    phno = Column(Integer, nullable=False)
    bloodgroup = Column(String(30))
    hospitalid = Column(Integer, ForeignKey('hospital.id'))
    hospital = relationship(Hospital, backref="bloodbank")


class BRequest(Base):
    __tablename__ = 'brequest'

    name = Column(String(50), primary_key=True)
    emailid = Column(String(30), primary_key=True)
    phno = Column(Integer, nullable=False)
    sex = Column(String(6), nullable=False)
    bloodgroup = Column(String(2), nullable=False)
    hospitalname = Column(String(50), nullable=False)


class Donor(Base):
    __tablename__ = 'donor'

    name = Column(String(20), primary_key=True)
    sex = Column(String(6), nullable=False)
    phno = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    bloodgroup = Column(String(3), nullable=False)
    address = Column(String(20), nullable=False)


class User(Base):
    __tablename__ = 'user'

    staffid = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    password= Column(String(50), nullable=False)


engine = create_engine('sqlite:///data.db')
#engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.create_all(engine)
