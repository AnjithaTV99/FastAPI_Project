# database.py

from config import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# SQLAlchemy model base
Base = declarative_base()

# Creating the SQLAlchemy engine using the configured database URL
engine = create_engine(DB_URL)

# Creating the databases.Database instance using the configured database URL
database = Database(DB_URL)

# Creating a SessionLocal class using sessionmaker and binding it to the SQLAlchemy engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseManager:
    def __init__(self, db_url: str = DB_URL):
        # Initialize DatabaseManager with a default or provided database URL
        self.engine = create_engine(db_url)
        self.database = Database(db_url)

    async def connect(self):
        # Connect to the database
        try:
            await self.database.connect()
        except Exception as e:
            # Log or handle the connection error appropriately
            print(f"Error connecting to the database: {e}")

    async def disconnect(self):
        # Disconnect from the database
        try:
            await self.database.disconnect()
        except Exception as e:
            # Log or handle the disconnection error appropriately
            print(f"Error disconnecting from the database: {e}")

# Create an instance of DatabaseManager
database_manager = DatabaseManager()
