from pydantic import BaseModel, EmailStr  # EmailStr auto-validates proper email format
from typing import Optional               # Used for optional fields (like in update requests)

# -------------------------------
# Base Schema (shared fields)
# -------------------------------

class UserBase(BaseModel):
    """
    Base class for shared user fields.
    Inherited by both Create and Output schemas.
    """
    name: str
    email: EmailStr
    age: int

# -------------------------------
# Request Schemas
# -------------------------------

class UserCreate(UserBase):
    """
    Schema used when creating a new user (POST).
    Inherits all required fields from UserBase.
    """
    pass

class UserUpdate(BaseModel):
    """
    Schema used when updating user info (PUT or PATCH).
    All fields are optional here to allow partial updates.
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

# -------------------------------
# Response Schema
# -------------------------------

class UserOut(UserBase):
    """
    Schema used when returning user info to client (GET).
    Adds ID field on top of UserBase and enables ORM mode.
    """
    id: int

    class Config:
        orm_mode = True  # Enables automatic conversion from SQLAlchemy model to Pydantic model
