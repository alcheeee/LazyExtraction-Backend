from sqlmodel import SQLModel, create_engine

sqlite_file = "database.db"
sqlite_url = f"sqlite:///{sqlite_file}"
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

