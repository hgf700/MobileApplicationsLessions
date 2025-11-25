from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import ENUM
from dotenv import load_dotenv
import os

load_dotenv() 

db=os.getenv("DATABASE")
postgres_passw=os.getenv("POSTGRES_PASSWORD")
postgres_user=os.getenv("POSTGRES_USER")

DATABASE_URL = f"postgresql+psycopg2://{postgres_user}:{postgres_passw}@localhost:5432/{db}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

user_type_enum = ENUM('client', 'courier', name='usertype', create_type=True)
user_type_enum.create(engine, checkfirst=True)

Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(user_type_enum, nullable=False)  # <-- poprawnie

    client_profile = relationship("Client", back_populates="user", uselist=False)
    courier_profile = relationship("Courier", back_populates="user", uselist=False)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String)

    user = relationship("User", back_populates="client_profile")
    shipments = relationship("Shipment", back_populates="client")

class Courier(Base):
    __tablename__ = "couriers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vehicle_number = Column(String)

    user = relationship("User", back_populates="courier_profile")
    shipments = relationship("Shipment", back_populates="courier")

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    courier_id = Column(Integer, ForeignKey("couriers.id"), nullable=True)
    pickup_address_let = Column(String)
    pickup_address_long = Column(String)
    delivery_address_let = Column(String)
    delivery_address_long = Column(String)
    status = Column(String, default="waiting")
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="shipments")
    courier = relationship("Courier", back_populates="shipments")
