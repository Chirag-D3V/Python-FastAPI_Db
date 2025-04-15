# -------------------------------
# Python Database (SQLAlchemy with SQLite) integration and CRUD Operations Cheat Sheet
# Author: Chirag Gupta
# Description: Core Python setup for Database (SQLAlchemy + SQLite) integration and CRUD operations with comments and examples
# -------------------------------

# -------------------------------
# Prerequisites and Setup
# -------------------------------

# 1. SQLAlchemy - A Python ORM (Object Relational Mapper) that allows you to interact with SQL databases using Python classes instead of raw SQL.
# 2. SQLite - A lightweight database stored in a single file — perfect for testing and development.
# 3. pyodbc - Used only if you're connecting to SQL Server. Not needed for SQLite.

# Setting and activating a virtual environment
# python -m venv myenv
# .\myenv\Scripts\activate    (Windows)

# Install required libraries
# pip install sqlalchemy

# Optionally, freeze dependencies into a requirements.txt
# pip freeze > requirements.txt

# -------------------------------
# Imports
# -------------------------------

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

# -------------------------------
# Important Notes:
# -------------------------------

#  The SQLite database file (systemdb.sqlite3) will be automatically created in the same directory
#     if it doesn't exist yet. No need to create it manually.

#  The 'check_same_thread=False' flag is specific to SQLite and prevents threading errors.
#     It allows SQLAlchemy sessions to be safely used across different parts of your code.

#  Unlike other DBs (MySQL, Postgres, SQL Server), SQLite needs no additional driver installations — 
#     it works out of the box with Python.

#  If you switch to SQL Server later, you'll need:
#     - pyodbc or pymssql
#     - Change the DATABASE_URL to match SQL Server format
#     - Probably adjust connection settings for driver and authentication

#  Summary of What This File Does:
# ----------------------------------
# | Task                        | Responsibility                                |
# |-----------------------------|-----------------------------------------------|
# | Define DB path              | Use os to dynamically locate the db file    |
# | Connect to DB               | create_engine with the DB URL               |
# | Set up base ORM class       | declarative_base() for all models           |
# | Create session factory      | SessionLocal for CRUD operations            |
# | Create tables               | create_tables() using SQLAlchemy metadata   |

# -------------------------------
#  BONUS: View Tables in SQLite DB Visually
# -------------------------------

#  I (Chirag Gupta) downloaded DB Browser for SQLite from:
#      https://sqlitebrowser.org/

# This tool allows you to open the systemdb.sqlite3 file and visually:
#     - Browse data in tables
#     - Inspect table schemas
#     - Run custom SQL queries
#     - Add/modify/delete data manually (for testing)

#  HOW TO USE IT:
# -----------------
# 1. Open DB Browser for SQLite
# 2. Click on “Open Database” and choose systemdb.sqlite3 from your project directory
# 3. Go to the “Browse Data” tab to see rows in your tables
# 4. Go to “Database Structure” to see which tables were created
# 5. Click on “Execute SQL” if you want to manually run any queries

# This is very useful for debugging or verifying if your Python code actually created the expected tables and data.

#  Pro Tip:
# If you're not seeing any tables:
#     → Double-check that your models file exists and that create_tables() is called