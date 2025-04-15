# -------------------------------
# models_and_app.py
# SQLAlchemy User Model + FastAPI Setup + Pydantic Schemas (Fully Explained)
# Author: Chirag Gupta
# -------------------------------

# ---------------------- IMPORTS ----------------------

from sqlalchemy import Column, Integer, String              # SQLAlchemy column types
from database import Base                                   # Base class from database.py for ORM model
from fastapi import FastAPI                                 # FastAPI web framework

# ---------------------- FASTAPI INSTANCE ----------------------

app = FastAPI()

# ---------------------- SQLALCHEMY MODEL ----------------------

# This class defines the table schema using SQLAlchemy ORM
class User(Base):
    __tablename__ = 'users'  # The table will be named 'users' in your SQLite DB

    id = Column(Integer, primary_key=True, index=True)        # Auto-incremented primary key
    name = Column(String, index=True)                         # Name field with index for faster search
    email = Column(String, unique=True, index=True)           # Unique email field (also indexed)
    age = Column(Integer)                                     # Age field (no indexing needed here)

