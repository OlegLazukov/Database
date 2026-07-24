from pydantic import BaseModel


class ConnectionPostgres(BaseModel):
    username: str = "postgres"
    password: str = "1039Gau41`*din"
    localhost: str = "localhost"
    port: int = 5432
    db: str = "trello"
