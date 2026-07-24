import pytest
from unittest.mock import MagicMock

from main import RedisConfig, RedisRepository


@pytest.fixture
def redis_repo():
    # Настраиваем конфигурацию и создаем экземпляр RedisRepository
    config = RedisConfig(host='localhost', port=6379, db=0)
    repo = RedisRepository(config)
    repo.redis_client = MagicMock()  # Мокируем Redis-клиент
    return repo


def test_set_user(redis_repo):
    user_id = 1
    full_name = "Петров Иван Сергеевич"

    redis_repo.set_user(user_id, full_name)

    # Проверяем, что метод set был вызван с правильным ключом и значением
    redis_repo.redis_client.set.assert_called_with('user:1', full_name)


def test_get_user(redis_repo):
    user_id = 1
    full_name = "Петров Иван Сергеевич"

    # Настройка возврата метода get
    redis_repo.redis_client.get.return_value = full_name.encode('utf-8')

    result = redis_repo.get_user(user_id)

    # Проверяем, что полученное значение соответствует ожидаемому
    assert result == full_name
    redis_repo.redis_client.get.assert_called_with('user:1')


def test_get_user_nonexistent(redis_repo):
    user_id = 2

    # Настройка возврата метода get на None
    redis_repo.redis_client.get.return_value = None

    result = redis_repo.get_user(user_id)

    # Проверяем, что возвращается ожидаемое сообщение
    assert result == "Такого пользователя - None не существует"
    redis_repo.redis_client.get.assert_called_with('user:2')


def test_delete_user(redis_repo):
    user_id = 1

    redis_repo.delete_user(user_id)

    # Проверяем, что метод delete был вызван с правильным ключом
    redis_repo.redis_client.delete.assert_called_with('user:1')