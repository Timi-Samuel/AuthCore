from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Base class for declarative class definitions
Base = declarative_base()

# Create an engine for SQLite database named 'users.db'
engine = create_engine(
    f"sqlite:///users.db",  # SQLite database file
    echo=True  # Enables SQL logging to console for debugging
)

# User table definition


class User(Base):
    __tablename__ = 'users'  # Table name in the database
    id = Column(Integer, primary_key=True)  # Auto-incrementing primary key
    email = Column(String)  # User email
    hashed_password = Column(String)  # User password (hashed)
    created_at = Column(DateTime)  # Account creation timestamp

# Verification codes table definition


class VerificationCodesTable(Base):
    __tablename__ = 'verification_codes'  # Table name in the database
    id = Column(Integer, primary_key=True)  # Auto-incrementing primary key
    email = Column(String)  # User email
    code = Column(String)  # Verification code sent to user
    password = Column(String)  # Password provided during signup (hashed)
    created_at = Column(DateTime)  # Timestamp when code was created


# Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables in the database if they do not exist
Base.metadata.create_all(engine)
