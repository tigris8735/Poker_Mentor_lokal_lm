from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    chips = Column(Integer, default=1500)
    level = Column(Integer, default=1)
    
class HandHistory(Base):
    __tablename__ = 'hand_histories'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    hand_data = Column(Text)  # JSON с данными раздачи
    analysis = Column(Text)   # Анализ от AI
    created_at = Column(DateTime, default=datetime.utcnow)