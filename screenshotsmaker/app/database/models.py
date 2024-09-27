import datetime
from enum import StrEnum

from sqlalchemy import BigInteger, String, BLOB, DateTime, Integer, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True


class CreatePPTTasks(Base):

    __tablename__ = 'create_ppt_tasks'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    client_uid: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    extra_data: Mapped[str] = mapped_column(String)
    ppt_template_hash: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    subtitle: Mapped[str] = mapped_column(String)
    footer: Mapped[str] = mapped_column(String)
    generated_text: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, nullable=False)
    status_message: Mapped[str] = mapped_column(String)
    ppt_template: Mapped[bytes] = mapped_column(LargeBinary)
    created_ppt_content: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow,
                                                          onupdate=datetime.datetime.utcnow)

    def __str__(self):
        return f'<CreatePPTTasks id={self.id} client_uid={self.client_uid} name={self.name}>'


class CreatePPTTasksSlides(Base):

    __tablename__ = 'create_ppt_tasks_slides'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    screenshot: Mapped[bytes] = mapped_column(LargeBinary)
    ppt_task_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    spreadsheet_screenshot: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow,
                                                          onupdate=datetime.datetime.utcnow)

    def __str__(self):
        return f'<CreatePPTTasksSlides id={self.id} position={self.position} title={self.title}>'


class CreateScreenshotTasksStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


TasksStatus = CreateScreenshotTasksStatus


class CreateScreenshotTasks(Base):

    __tablename__ = 'create_screenshot_tasks'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    client_uid: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    extra_data: Mapped[str] = mapped_column(String)
    content_hash: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    status_message: Mapped[str] = mapped_column(String)
    content: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow,
                                                          onupdate=datetime.datetime.utcnow)

    def __str__(self):
        return f'<CreateScreenshotTasks id={self.id} client_uid={self.client_uid} name={self.name}>'


class CreateScreenshotTasksScreenshots(Base):

    __tablename__ = 'create_screenshot_tasks_screenshots'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    screenshot_task_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow,
                                                          onupdate=datetime.datetime.utcnow)

    def __str__(self):
        return f'<CreateScreenshotTasksScreenshots id={self.id} position={self.position}>'


class DuplicatePPTSlidesTask(Base):

    __tablename__ = 'duplicate_ppt_slides_tasks'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    client_uid: Mapped[str] = mapped_column(String, nullable=False)
    extra_data: Mapped[str] = mapped_column(String)
    ppt_in: Mapped[bytes] = mapped_column(LargeBinary)
    ppt_out: Mapped[bytes] = mapped_column(LargeBinary)
    target_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    status_message: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow,
                                                          onupdate=datetime.datetime.utcnow)

