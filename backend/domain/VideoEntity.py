from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func

from domain.Base import Base


class VideoEntity(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    filename = Column('filename', String(256))
    title = Column('title', String(64))
    content = Column('content', Text)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, filename, title, content):
        self.filename = filename
        self.title = title
        self.content = content
