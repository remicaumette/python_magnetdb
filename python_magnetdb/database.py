from os import getenv

from sqlmodel import Session, create_engine

from orator import DatabaseManager, Schema, Model

connect_args = {"check_same_thread": False}
engine = create_engine(getenv("DATABASE_URL") or "sqlite:///magnets.db", echo=False, connect_args=connect_args)

config = {
    'postgres': {
        'driver': 'postgres',
        'host': getenv('DATABASE_HOST') or 'localhost',
        'database': getenv('DATABASE_NAME') or 'magnetdb',
        'user': getenv('DATABASE_USER') or 'magnetdb',
        'password': getenv('DATABASE_PASSWORD') or 'magnetdb',
        'prefix': ''
    }
}

db = DatabaseManager(config)
schema = Schema(db)
Model.set_connection_resolver(db)


def perform_migrations():
    pass

def get_session():
    with Session(engine) as session:
        yield session
