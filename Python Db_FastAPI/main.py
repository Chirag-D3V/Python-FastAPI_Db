# # -------------------------------
# # Python CRUD Application for Managing Users
# # Author: Chirag Gupta
# # Description: A command-line Python application for CRUD operations (Create, Read, Update, Delete) using SQLAlchemy
# # -------------------------------

# # -------------------------------
# # Imports
# # -------------------------------

# # Import necessary functions and classes
# from database import SessionLocal, create_tables           # Import session and table creation functions
# from crud import create_user, get_user_by_id, update_user, delete_user  # Import CRUD operations for users

# # -------------------------------
# # Function to Display CRUD Menu
# # -------------------------------

# def display_menu():
#     """
#     This function displays the menu with available choices for CRUD operations.
#     """
#     print("\n========= CRUD Menu =========")
#     print("1. Create User")
#     print("2. Get User by ID")
#     print("3. Update User")
#     print("4. Delete User")
#     print("5. Exit")
#     print("=============================")

# # -------------------------------
# # Main Function
# # -------------------------------

# def main():
#     """
#     This is the main function where the application runs.
#     - It establishes a session with the database.
#     - Loops through the menu options for performing CRUD operations.
#     """
#     # Step 1: Ensure the database and tables are created
#     create_tables()  # Call to `create_tables` function to create tables if not exist

#     # Step 2: Create a new session for interacting with the database
#     db_session = SessionLocal()  # Initialize a session to communicate with the DB

#     while True:  # Start an infinite loop to keep the application running until the user chooses to exit
#         display_menu()  # Display CRUD options to the user
#         choice = input("Enter your choice (1-5): ")  # Get user input for their choice

#         # Step 3: Handling different choices for CRUD operations

#         if choice == "1":
#             # Create a new user
#             name = input("Enter name: ")
#             email = input("Enter email: ")
#             age = int(input("Enter age: "))
#             user = create_user(db_session, name, email, age)  # Create user in DB
#             print(f" User created: ID={user.id}, Name={user.name}")  # Output the created user details

#         elif choice == "2":
#             # Get a user by ID
#             user_id = int(input("Enter user ID to fetch: "))
#             user = get_user_by_id(db_session, user_id)  # Fetch user by ID
#             if user:
#                 print(f"👤 User Found - ID: {user.id}, Name: {user.name}, Email: {user.email}, Age: {user.age}")
#             else:
#                 print("❌ User not found.")  # If no user found with that ID

#         elif choice == "3":
#             # Update an existing user's information
#             user_id = int(input("Enter user ID to update: "))
#             name = input("Enter new name: ")
#             email = input("Enter new email: ")
#             age = int(input("Enter new age: "))
#             user = update_user(db_session, user_id, name, email, age)  # Update user data
#             if user:
#                 print(f"🔁 User updated: ID={user.id}, Name={user.name}")  # Output the updated user details
#             else:
#                 print("❌ User not found to update.")  # If no user found to update

#         elif choice == "4":
#             # Delete a user by ID
#             user_id = int(input("Enter user ID to delete: "))
#             user = delete_user(db_session, user_id)  # Delete the user from DB
#             if user:
#                 print(f"🗑️ User deleted: ID={user.id}, Name={user.name}")  # Output the deleted user details
#             else:
#                 print("❌ User not found to delete.")  # If no user found to delete

#         elif choice == "5":
#             # Exit the program
#             print("👋 Exiting... Goodbye!")  # Goodbye message when user opts to exit
#             break  # Break out of the infinite loop, ending the program

#         else:
#             # Invalid choice entered
#             print("⚠️ Invalid choice. Please enter 1-5.")  # Error message for invalid input

#     db_session.close()  # Close the session to release database connection

# # -------------------------------
# # Run the Application
# # -------------------------------

# if __name__ == "__main__":
#     """
#     Entry point of the application when the script is executed.
#     """
#     main()  # Call the main function to run the program


# ----------------------------------------------------------------------- main.py ---------------------------------------------------------------
# -------------------------------
# FastAPI Application (CRUD with SQLAlchemy Integration)
# Author: Chirag Gupta
# Description: Core FastAPI app with SQLAlchemy database integration for CRUD operations with detailed explanations
# -------------------------------

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables  # Importing the DB session and table creation function
import crud, schemas  # Import CRUD operations, ORM models, and Pydantic schemas

# Create FastAPI app instance
app = FastAPI()

# -------------------------------
# FastAPI Event Handling
# -------------------------------

#  FastAPI allows you to run functions at specific points during the application lifecycle.
# In this case, we'll run the create_tables() function when the app starts up.

# @app.on_event("startup")
# def on_startup():
#     """
#     This function is called when the app starts up.
#     It ensures that the database tables are created before the app handles requests.
#     """
#     create_tables()  # Create all the tables in the database

# -------------------------------
# Dependency to Get DB Session
# -------------------------------

# FastAPI's Depends() function allows us to inject the DB session into the route functions automatically.
# get_db() will handle session management (i.e., opening and closing DB sessions) for us.

def get_db():
    """
    This dependency function provides a fresh DB session for each request.
    It ensures that the DB session is properly closed after the request is completed.
    """
    """
     What does yield do here?
    - yield pauses the function and returns the database session (db) to the FastAPI route handler.
    - The route can then use this session to interact with the database.
    - Once the request is processed, the function resumes after yield and closes the session to ensure proper cleanup.
    - yield essentially allows FastAPI to inject the database session into the route while maintaining control over the session lifecycle.

    This ensures that we do not manually open or close sessions within each route, simplifying session management.
    """
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session so it can be used in the route function
    finally:
        db.close()  # Close the session after the request is done

# -------------------------------
# CRUD Routes
# -------------------------------

# These routes handle incoming HTTP requests and invoke the appropriate CRUD operations.

# 1. Create a new user
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    This route creates a new user in the database.
    It receives the user data in the request body (using Pydantic schema UserCreate),
    calls the create_user function in CRUD, and returns the newly created user.
    """
    return crud.create_user(db, user.name, user.email, user.age)

# 2. Read a user by ID
@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    This route fetches a user by their ID.
    It calls the get_user_by_id function from CRUD, and returns the user.
    If no user is found, it raises a 404 error with a custom message.
    """
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 3. Update user info
@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user_route(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    This route updates an existing user.
    It takes the user ID and updated details from the request body,
    and calls the update_user function from CRUD to update the user in the database.
    """
    db_user = crud.update_user(db, user_id, user.name, user.email, user.age)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 4. Delete a user by ID
@app.delete("/users/{user_id}", response_model=schemas.UserOut)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """
    This route deletes a user from the database based on their ID.
    It calls the delete_user function from CRUD and deletes the user.
    If the user doesn't exist, it raises a 404 error.
    """
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# -------------------------------
# Important Notes:
# -------------------------------

#  App Lifecycle:
# - FastAPI provides event hooks (e.g., @app.on_event("startup")) to run functions during specific stages of the app's lifecycle.
# - In this case, the on_startup function is used to create the tables in the database as soon as the app starts.

#  Dependency Injection:
# - FastAPI uses the Depends() function to handle dependencies like database sessions.
# - When a route function requires access to the database, the get_db() function is called, which provides a fresh DB session.
# - After the request is processed, the DB session is automatically closed.

#  CRUD Operations:
# - The routes are connected to the CRUD operations that are imported from the crud.py file.
# - Each route function handles specific HTTP methods (GET, POST, PUT, DELETE) and invokes the corresponding CRUD operation.

#  Session Management:
# - SessionLocal() creates a new session object, which is used to interact with the database.
# - It's important to close the session after each request to release the database connection, which is handled in the finally block of get_db().

# -------------------------------
#  BONUS: View Data and Tables in SQLite
# -------------------------------

#  After running this FastAPI app and making some requests, you can visualize the data created in the SQLite database.

# If you're using DB Browser for SQLite, follow these steps to see your database tables:
# 1. Open DB Browser for SQLite (download from https://sqlitebrowser.org/)
# 2. Click on “Open Database” and select systemdb.sqlite3 (the database created by this FastAPI app)
# 3. In the “Database Structure” tab, you will see the tables that have been created (e.g., users table)
# 4. You can view the table's content in the “Browse Data” tab, which will show all the records in the table.
# 5. You can also run custom SQL queries to check the data using the “Execute SQL” tab.

#  Pro Tip:
# After each API request (e.g., creating or deleting users), check the database to confirm the changes.
# This is an excellent way to visualize how your FastAPI app is interacting with the database.

#  Remember:
# - You need to ensure that your tables are created during startup (on_startup()), and that they match the models defined in models.py.
# - DB Browser for SQLite provides a clean, visual way to interact with and inspect your SQLite database.
