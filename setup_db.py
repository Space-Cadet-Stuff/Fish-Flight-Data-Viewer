from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import check_password_hash
from sqlalchemy.types import DateTime
from datetime import datetime

Base = declarative_base()# Base class for ORM models

class User(Base):# User model
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def check_password(self, password):# Method to check password
        return check_password_hash(self.password, password)

class CSVFile(Base):
    __tablename__ = 'csv_files'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    title = Column(String, nullable=False)
    launch_date = Column(String)  # You can use Date if you want stricter typing
    engine_class = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    upload_time = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="csv_files")

engine = create_engine('sqlite:///datalogger.db')# Database setup

Base.metadata.create_all(engine)

print('Database and tables created successfully')