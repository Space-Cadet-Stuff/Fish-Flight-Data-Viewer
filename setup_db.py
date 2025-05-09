from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import check_password_hash
from sqlalchemy.types import DateTime

Base = declarative_base()# Base class for ORM models

class User(Base):# User model
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def check_password(self, password):# Method to check password
        return check_password_hash(self.password, password)

engine = create_engine('sqlite:///todo.db')# Database setup

Base.metadata.create_all(engine)

print('Database and tables created successfully')