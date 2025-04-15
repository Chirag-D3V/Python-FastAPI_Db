# -------------------------------
# CRUD Operations (Create, Read, Update, Delete)
# Author: Chirag Gupta
# Description: Core CRUD operations on the User model using SQLAlchemy ORM
# -------------------------------

from sqlalchemy.orm import session                  # Session from SQLAlchemy to interact with the DB
from models import User                              # User model (table) imported for CRUD operations

# -------------------------------
# Inserting a new user in the database
# -------------------------------
def create_user(db_session: session, name: str, email: str, age: int):
    """
    Adds a new user to the database.

    Parameters:
    - db_session: Active session to interact with the DB.
    - name (str): Name of the user.
    - email (str): Email of the user.
    - age (int): Age of the user.

    Returns:
    - db_user: The created user object if successful.
    - None: If an error occurs during the insertion.
    """
    db_user = User(name=name, email=email, age=age)  # Create a new user instance
    
    try:
        db_session.add(db_user)  # Add the user to the session (pending commit)
        db_session.commit()      # Commit the transaction to the database (i.e., insert the user)
        db_session.refresh(db_user)  # Ensure the user instance is updated with DB-generated values (like ID)
        return db_user           # Return the user object (with the assigned ID after commit)
    
    except Exception as e:
        db_session.rollback()    # Rollback any changes in case of an error (to maintain DB consistency)
        print(f"Error occurred: {e}")  # Print the error for debugging (in real apps, use logging)
        return None               # Return None indicating failure

# -------------------------------
# Fetching a user by ID from the database
# -------------------------------
def get_user_by_id(db_session: session, user_id: int):
    """
    Fetch a user by their ID.

    Parameters:
    - db_session: Active session to interact with the DB.
    - user_id (int): ID of the user to fetch.

    Returns:
    - User object if found, otherwise None.
    """
    return db_session.query(User).filter(User.id == user_id).first()  # Query the database for the user by ID

# -------------------------------
# Updating user information
# -------------------------------
def update_user(db_session: session, user_id: int, name: str, email: str, age: int):
    """
    Updates an existing user's details.

    Parameters:
    - db_session: Active session to interact with the DB.
    - user_id (int): ID of the user to update.
    - name (str): New name of the user.
    - email (str): New email of the user.
    - age (int): New age of the user.

    Returns:
    - db_user: The updated user object if successful.
    - None: If the user is not found or an error occurs.
    """
    db_user = db_session.query(User).filter(User.id == user_id).first()  # Fetch the user by ID
    
    if db_user:
        try:
            # Update the user's attributes
            db_user.name = name
            db_user.email = email
            db_user.age = age
            
            db_session.commit()    # Commit the changes to the DB
            db_session.refresh(db_user)  # Refresh the instance with updated data from DB
            return db_user          # Return the updated user object
        
        except Exception as e:
            db_session.rollback()  # Rollback if any exception occurs
            print(f"Error occurred: {e}")  # Print the error for debugging
            return None             # Return None indicating failure
    else:
        return None  # Return None if the user wasn't found

# -------------------------------
# Deleting a user from the database
# -------------------------------
def delete_user(db_session: session, user_id: int):
    """
    Deletes a user from the database by their ID.

    Parameters:
    - db_session: Active session to interact with the DB.
    - user_id (int): ID of the user to delete.

    Returns:
    - db_user: The deleted user object if successful.
    - None: If the user is not found or an error occurs.
    """
    db_user = db_session.query(User).filter(User.id == user_id).first()  # Fetch the user by ID
    
    if db_user:
        try:
            db_session.delete(db_user)  # Mark the user for deletion
            db_session.commit()         # Commit the transaction (deletes the user)
            return db_user              # Return the deleted user object
        
        except Exception as e:
            db_session.rollback()      # Rollback if any exception occurs
            print(f"Error occurred: {e}")  # Print the error for debugging
            return None                 # Return None indicating failure
    else:
        return None  # Return None if the user wasn't found

# -------------------------------
# Important Notes:
# -------------------------------
# - db_session.refresh(): 
#     This method ensures that after committing or updating data, the instance is synchronized with the latest database values (e.g., the auto-generated ID after a user is inserted).
#     It's especially important in the case of operations like `create_user()` or `update_user()` where changes are committed to the DB.

# - Error Handling (try-except):
#     The try-except block prevents the application from crashing in case of errors (like constraint violations, database connectivity issues, or invalid input). 
#     Any exception is caught, the transaction is rolled back, and the error message is logged.
#     Rollback ensures that partial or invalid data doesn't get committed to the database.

# -------------------------------
# Summary Table of Operations
# -------------------------------
'''
| Operation         | Description                                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| `create_user()`   | Adds a new user to the database, commits, and returns the created user with assigned ID     |
| `get_user_by_id()`| Fetches a user by ID from the database, returns the user object or None if not found        |
| `update_user()`   | Updates a user's details, commits the changes, and returns the updated user object          |
| `delete_user()`   | Deletes a user from the database, commits the deletion, and returns the deleted user object |
'''