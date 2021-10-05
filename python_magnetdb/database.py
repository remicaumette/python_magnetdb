from typing import Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

sqlite_file_name = "magnets.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# version sans fastapi: engine = create_engine(sqlite_url, echo=True)
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

