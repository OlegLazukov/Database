import redis
from pydantic import BaseModel, Field, ValidationError

class RedisConfig(BaseModel):
    host: str = Field(default='localhost', description="Redis хост")
    port: int = Field(default=6379, description="Redis порт")
    db: int = Field(default=0, description="Номер базы данных Redis")


class RedisRepository:
    def __init__(self, config: RedisConfig):
        self.redis_client = redis.Redis(host=config.host, port=config.port, db=config.db)

    def set_user(self, user_id: int, full_name: str) -> None:
        key = f'user:{user_id}'
        self.redis_client.set(key, full_name)

    def get_user(self, user_id: int) -> str:
        key = f'user:{user_id}'
        full_name = self.redis_client.get(key)

        if full_name is None:
            return f"Такого пользователя - {full_name} не существует"

        return full_name.decode('utf-8')

    def delete_user(self, user_id: int) -> None:
        key = f'user:{user_id}'
        self.redis_client.delete(key)


try:
    config = RedisConfig(host='localhost', port=6379, db=0)
    redis_repo = RedisRepository(config)

    redis_repo.set_user(1, "Петров Иван Сергеевич")

    user_full_name = redis_repo.get_user(1)
    print(user_full_name)

    redis_repo.delete_user(1)

    user_full_name_after_delete = redis_repo.get_user(1)
    print(user_full_name_after_delete)
except ValidationError as e:
    print(e)