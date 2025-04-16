from sqlalchemy import create_engine                      # Used to create the DB engine (connection to the DB)
from sqlalchemy.ext.declarative import declarative_base   # Base class for ORM models (tables)
from sqlalchemy.orm import sessionmaker                   # Creates sessions for DB transactions
import os                                                 # Used to dynamically construct the DB file path

# -------------------------------
# SQLite DB Configuration
# -------------------------------

# Get the absolute directory path of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the SQLite database file path (in the same directory as this Python script)
DB_PATH = os.path.join(BASE_DIR, "systemdb.sqlite3")

# Construct the SQLAlchemy Database URL for SQLite
# Format: "sqlite:///<absolute_path_to_db>"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# -------------------------------
# SQLAlchemy Engine & Session Setup
# -------------------------------

# Create an engine connected to the SQLite DB
# connect_args={"check_same_thread": False} allows multiple threads to use the same connection (required for SQLite)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a Base class for ORM models to inherit from
Base = declarative_base()

# Create a session factory bound to the engine
# autocommit=False → You need to explicitly commit changes
# autoflush=False → Prevents auto flushing pending changes to the DB before queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# -------------------------------
# Table Creation Function
# -------------------------------
# This function creates all tables defined in ORM models that inherit from Base
def create_tables():
    Base.metadata.create_all(bind=engine)
