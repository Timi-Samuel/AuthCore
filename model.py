from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
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


class VerificationLogs(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    email = Column(String)  # User email
    # Is verification still pending or successful?
    successful = Column(Boolean, default=False)
    # Timestamp when account was officially verified
    time_verified = Column(DateTime)


# Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables in the database if they do not exist
Base.metadata.create_all(engine)


class DBOperations:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def record_verif_attempt(self, timestamp, code):
        user_verifcation_attempt = VerificationCodesTable(
            email=self.email, password=self.password, code=code, created_at=timestamp)
        session.add(user_verifcation_attempt)
        session.commit()
        return

    def remove_verification_code(self):
        target = session.query(VerificationCodesTable).filter_by(
            email=self.email).all()
        for i in target:
            session.delete(i)
        return
