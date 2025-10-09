import sqlite3
import logging
from datetime import datetime
from config.settings import DATABASE_URL

class Database:
    def __init__(self):
        self.connection = None
        
    def get_connection(self):
        """Создает соединение с базой данных"""
        if self.connection is None:
            # Извлекаем путь к БД из DATABASE_URL
            db_path = DATABASE_URL.replace('sqlite:///', '')
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def init_db(self):
        """Инициализирует таблицы в базе данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ai_requests INTEGER DEFAULT 0,
                hand_analysis INTEGER DEFAULT 0
            )
        ''')
        
        # Таблица запросов к AI
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                prompt TEXT,
                response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        logging.info("✅ База данных инициализирована")
    
    def save_user(self, user_id: int, username: str = None, first_name: str = None):
        """Сохраняет или обновляет пользователя в базе данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, username, first_name)
                VALUES (?, ?, ?)
            ''', (user_id, username, first_name))
            conn.commit()
            logging.info(f"✅ Пользователь {user_id} сохранен в БД")
        except Exception as e:
            logging.error(f"❌ Ошибка сохранения пользователя: {e}")
    
    def increment_ai_requests(self, user_id: int):
        """Увеличивает счетчик запросов к AI для пользователя"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET ai_requests = ai_requests + 1 
                WHERE user_id = ?
            ''', (user_id,))
            conn.commit()
        except Exception as e:
            logging.error(f"❌ Ошибка увеличения счетчика AI: {e}")
    
    def increment_hand_analysis(self, user_id: int):
        """Увеличивает счетчик анализов раздач для пользователя"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET hand_analysis = hand_analysis + 1 
                WHERE user_id = ?
            ''', (user_id,))
            conn.commit()
        except Exception as e:
            logging.error(f"❌ Ошибка увеличения счетчика анализов: {e}")
    
    def get_user_stats(self, user_id: int) -> dict:
        """Возвращает статистику пользователя"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT ai_requests, hand_analysis, registration_date 
                FROM users 
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'ai_requests': result['ai_requests'],
                    'hand_analysis': result['hand_analysis'],
                    'registration_date': result['registration_date']
                }
            else:
                # Если пользователь не найден, создаем его
                self.save_user(user_id)
                return {
                    'ai_requests': 0,
                    'hand_analysis': 0,
                    'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
        except Exception as e:
            logging.error(f"❌ Ошибка получения статистики: {e}")
            return {
                'ai_requests': 0,
                'hand_analysis': 0,
                'registration_date': 'Неизвестно'
            }
    
    def save_ai_request(self, user_id: int, prompt: str, response: str):
        """Сохраняет запрос и ответ AI в базу данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO ai_requests (user_id, prompt, response)
                VALUES (?, ?, ?)
            ''', (user_id, prompt, response))
            conn.commit()
        except Exception as e:
            logging.error(f"❌ Ошибка сохранения запроса AI: {e}")
    
    def close(self):
        """Закрывает соединение с базой данных"""
        if self.connection:
            self.connection.close()
            self.connection = None