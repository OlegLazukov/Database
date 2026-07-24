from sqlalchemy import create_engine
from src.models.model import Base
from src.connections.postgres import ConnectionPostgres
from sqlalchemy.exc import SQLAlchemyError




if __name__ == "__main__":
    try:
        con = ConnectionPostgres()
        engine = create_engine(f'postgresql://{con.username}:{con.password}@{con.localhost}:{con.port}/{con.db}')
        Base.metadata.create_all(engine)
    except SQLAlchemyError as e:
        print(f"Ошибка {e}")