from sqlalchemy import Column, String, Integer
from .database import Base


class TodoModel(Base):
    __tablename__ = 'sql_todo_app'
    
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, unique=True, index=True)