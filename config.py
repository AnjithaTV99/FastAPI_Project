# config.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Database configuration

# Get the database user from the environment variables, default to "default_user" if not set
DB_USER = os.getenv("DB_USER", "default_user")

# Get the database password from the environment variables, default to "default_password" if not set
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")

# Get the database name from the environment variables, default to "default_database" if not set
DB_NAME = os.getenv("DB_NAME", "default_database")

# Build the database URL using the retrieved environment variables
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}"
