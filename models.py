# models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# SQLAlchemy model base
Base = declarative_base()

class User(Base):
    # User model representing the 'users' table
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String, index=True)

    # Establishing a relationship with the 'Profile' model
    profile = relationship("Profile", back_populates="user")

class Profile(Base):
    # Profile model representing the 'profiles' table
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    profile_picture = Column(String)
    
    # Creating a foreign key relationship with the 'User' model
    user_id = Column(Integer, ForeignKey("users.id"))

    # Establishing a relationship with the 'User' model
    user = relationship("User", back_populates="profile")
