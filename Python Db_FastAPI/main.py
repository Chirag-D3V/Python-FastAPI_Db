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
