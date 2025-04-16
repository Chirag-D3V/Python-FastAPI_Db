from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables  # Importing the DB session and table creation function
import crud, schemas  # Import CRUD operations, ORM models, and Pydantic schemas

# Create FastAPI app instance
app = FastAPI()

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
