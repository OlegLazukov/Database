import uuid
from sqlalchemy import String, DateTime, ForeignKey, Text, Date, Index, text, create_engine
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
from typing import Annotated

# Создаем базовый класс для всех моделей
Base = declarative_base()

int_pk = Annotated[UUID ,mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]
str_name_uq = Annotated[str, mapped_column(String(100), nullable=False, unique=True)]
str_name = Annotated[str, mapped_column(String(100), nullable=False)]

# Определяем Enum для статуса задачи
class TaskStatus(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

# Модель User
class User(Base):
    __tablename__ = 'user'

    id: Mapped[int_pk]
    full_name: Mapped[str_name]
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)  # email, не может быть пустым и уникален
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)  # дата создания записи

    # Связь с задачами, автором которых является этот пользователь
    tasks: Mapped[list["Task"]] = relationship('Task', back_populates='author')

# Модель Task
class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)  # заголовок задачи
    description: Mapped[str] = mapped_column(Text)  # описание задачи
    status: Mapped[TaskStatus]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=False)  # дата создания задачи
    author_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id', ondelete="CASCADE"), nullable=False)  # ID автора задачи

    # Связь с пользователем-автором задачи
    author: Mapped[User] = relationship('User', back_populates='tasks')

Index('idx_task_author', Task.author_id)  # индекс по полю author_id

# Модель Board
class Board(Base):
    __tablename__ = 'board'

    id: Mapped[int_pk]
    name: Mapped[str_name_uq]

# Модель Column
class Column(Base):
    __tablename__ = 'column'

    id: Mapped[int_pk]
    name: Mapped[str_name]
    board_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('board.id', ondelete="CASCADE"), nullable=False)

# Модель Sprint
class Sprint(Base):
    __tablename__ = 'sprint'

    id: Mapped[int_pk]
    name: Mapped[str_name]
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)

# Модель Group
class Group(Base):
    __tablename__ = 'group'

    id: Mapped[int_pk]
    name: Mapped[str_name_uq]

# Создаем движок и базу данных
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')
Base.metadata.create_all(engine)  # создаем все таблицы в базе данных

