# -------------------------------
# Basic SQLAlchemy CRUD Test Runner
# Author: Chirag Gupta
# Description: Runs CRUD operations in sequence to test the database setup.
# Just run app.py — the user will be created, fetched, updated, and deleted.
# -------------------------------

# ---------------------- IMPORTS ----------------------

import logging  # For structured log output instead of raw print statements
from sqlalchemy.orm import Session  # Typing hint for database session
from typing import Optional  # For safe type hints

# Local project imports
from database import SessionLocal, create_tables  # DB setup helpers
from crud import create_user, get_user_by_id, update_user, delete_user  # User operations

# ---------------------- LOGGING SETUP ----------------------

# Configure logging: INFO level shows info + warnings + errors
# Format includes timestamp, log level, and message
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# ---------------------- MAIN FUNCTION ----------------------

def main() -> None:
    """
    Main function to sequentially run and verify all basic CRUD operations:
    - Create a user
    - Fetch user by ID
    - Update user details
    - Delete user
    This helps confirm that your SQLAlchemy + DB setup is working correctly.
    """
    db_session: Optional[Session] = None  # Declare session for finally block

    try:
        # STEP 1: Create tables if not already present
        create_tables()
        logging.info(" Database tables created or already exist.")

        # STEP 2: Start a new DB session
        db_session = SessionLocal()

        # STEP 3: Create a new user
        user = create_user(db_session, "Chirag", "chirag@gmail.com", 24)
        logging.info(f" User Created → ID: {user.id}, Name: {user.name}, Email: {user.email}")

        # STEP 4: Fetch the user by ID
        user_from_db_by_id = get_user_by_id(db_session, user.id)
        logging.info(f" User Fetched → ID: {user_from_db_by_id.id}, Name: {user_from_db_by_id.name}")

        # STEP 5: Update the user's name
        updated_user = update_user(db_session, user.id, "Chirag Gupta", "chirag@gmail.com", 24)
        logging.info(f" User Updated → ID: {updated_user.id}, Name: {updated_user.name}")

        # STEP 6: Delete the user
        deleted_user = delete_user(db_session, user.id)
        logging.info(f" User Deleted → ID: {deleted_user.id}, Name: {deleted_user.name}")

    except Exception as e:
        logging.error(" An error occurred during CRUD operations.", exc_info=True)

    finally:
        if db_session:
            db_session.close()
            logging.info(" Database session closed.")

# ---------------------- EXECUTION ENTRY POINT ----------------------

# This ensures the main function only runs when the script is executed directly
if __name__ == "__main__":
    main()
