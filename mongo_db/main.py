from pymongo import MongoClient
from bson import ObjectId
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class Task(BaseModel):
    title: str
    tags: List[str] = Field(default_factory=list)
    owner: str
    comments: List[str] = Field(default_factory=list)
    custom_fields: Optional[Dict[str, str]] = None


class MongoTaskRepository:
    def __init__(self, connection_string: str, db_name: str, collection_name: str):
        """Инициализация подключения к MongoDB."""
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_task(self, data: Task) -> str:
        """Создает новую задачу и возвращает ID вставленного документа."""
        result = self.collection.insert_one(data.model_dump())
        return str(result.inserted_id)

    def get_task_by_id(self, task_id: str) -> Optional[dict]:
        """Получает задачу по ID."""
        task = self.collection.find_one({"_id": ObjectId(task_id)})
        return task

    def delete_task(self, task_id: str) -> bool:
        """Удаляет задачу по ID, возвращает True, если успешно."""
        result = self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0

    def aggregate_by_tags(self) -> List[dict]:
        """Группирует задачи по тегам и считает их количество."""
        pipeline = [
            {
                "$unwind": "$tags"
            },
            {
                "$group": {
                    "_id": "$tags",
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "tag": "$_id",
                    "count": "$count",
                    "_id": False
                }
            }
        ]
        return list(self.collection.aggregate(pipeline))


# Пример использования
if __name__ == "__main__":
    mongo_repo = MongoTaskRepository("mongodb://localhost:27017/", "task_db", "tasks")

    # Создание задачи
    new_task_data = Task(
        title="Первая задача",
        tags=["work", "urgent"],
        owner="kein@google.com",
        comments=["Комментарий 1", "Комментарий 2"],
        custom_fields={"priority": "high"}
    )

    task_id = mongo_repo.create_task(new_task_data)
    print(f"Создана задача с ID: {task_id}")

    # Получение задачи по ID
    task = mongo_repo.get_task_by_id(task_id)
    print(f"Полученная задача: {task}")

    # Удаление задачи
    success = mongo_repo.delete_task(task_id)
    print(f"Задача удалена: {success}")

    # Агрегация задач по тегам
    tags_summary = mongo_repo.aggregate_by_tags()
    print("Количество задач по тегам:", tags_summary)