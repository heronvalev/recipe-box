from pathlib import Path
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine


# Define the SQLite database file path.
sqlite_file_path = Path("data/recipes.db")

# Build the database URL from the file path.
DATABASE_URL = f"sqlite:///{sqlite_file_path}"

# Ensure the database folder exists before SQLite tries to create the file.
sqlite_file_path.parent.mkdir(parents=True, exist_ok=True)

# Create the SQLModel engine used to talk to the database.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Create all database tables from SQLModel models.
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


# Provide a database session for each request.
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session