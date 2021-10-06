from typing import Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

sqlite_file_name = "magnets.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# version sans fastapi: engine = create_engine(sqlite_url, echo=True)
connect_args = {"check_same_thread": False}

# set echo to False to avoid SQL messages
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session


