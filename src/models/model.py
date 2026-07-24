import uuid
from sqlalchemy import String, DateTime, ForeignKey, Text, Date, Index, text
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from src.enums.task_status import TaskStatus
from typing import Annotated

Base = declarative_base()

int_pk = Annotated[UUID ,mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]
str_name_uq = Annotated[str, mapped_column(String(100), nullable=False, unique=True)]
str_name = Annotated[str, mapped_column(String(100), nullable=False)]


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int_pk]
    full_name: Mapped[str_name]
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    tasks: Mapped[list["Task"]] = relationship('Task', back_populates='author')


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = (Index('idx_task_author', "author_id",unique=True),)
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=False)
    author_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    author: Mapped[User] = relationship('User', back_populates='tasks')



class Board(Base):
    __tablename__ = 'board'

    id: Mapped[int_pk]
    name: Mapped[str_name_uq]

class Column(Base):
    __tablename__ = 'column'

    id: Mapped[int_pk]
    name: Mapped[str_name]
    board_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('board.id', ondelete="CASCADE"), nullable=False)

class Sprint(Base):
    __tablename__ = 'sprint'

    id: Mapped[int_pk]
    name: Mapped[str_name]
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)


class Group(Base):
    __tablename__ = 'group'

    id: Mapped[int_pk]
    name: Mapped[str_name_uq]