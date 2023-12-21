# main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import database_manager, SessionLocal
from models import Base, User, Profile
from passlib.context import CryptContext
import logging

app = FastAPI()

# Dependency to get the database session
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=database_manager.engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User Registration Endpoint
@app.post("/register")
async def register_user(
    full_name: str, 
    email: str, 
    password: str, 
    phone: str, 
    profile_picture: str = None,
    db: Session = Depends(get_db)
):
    try:
        # Check if the user with the given email or phone already exists
        existing_user = db.query(User).filter((User.email == email) | (User.phone == phone)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email or phone already registered")

        # Hash the user's password
        hashed_password = pwd_context.hash(password)

        # Create a new user
        new_user = User(full_name=full_name, email=email, password=hashed_password, phone=phone)
        db.add(new_user)
        db.commit()

        # Create a new profile for the user
        new_profile = Profile(user_id=new_user.id, profile_picture=profile_picture)
        db.add(new_profile)
        db.commit()

        return {"message": "User registered successfully"}

    except HTTPException as he:
        raise he

    except Exception as e:
        # Log the exception and raise a server error
        logger = logging.getLogger(__name__)
        logger.error(f"Exception during user registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get User Details Endpoint
@app.get("/user/{user_id}")
async def get_user_details(user_id: int, db: Session = Depends(get_db)):
    try:
        # Retrieve the user with the given user_id
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Retrieve the profile associated with the user
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()

        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        return {"user": user, "profile": profile}

    except Exception as e:
        # Log the exception and raise a server error
        logger = logging.getLogger(__name__)
        logger.error(f"Exception during user details retrieval: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
