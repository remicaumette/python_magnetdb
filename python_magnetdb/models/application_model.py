from sqlalchemy.orm import declarative_base
from uuid import uuid4

ApplicationModel = declarative_base()


def generate_uuid():
    return str(uuid4())
