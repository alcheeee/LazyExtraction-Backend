from sqlmodel import SQLModel, create_engine
from ..config import settings

connect_args = {"check_same_thread": False}
engine = create_engine(settings.SQLITE_URL, connect_args=connect_args)

def initialize_db():
    SQLModel.metadata.create_all(engine)

