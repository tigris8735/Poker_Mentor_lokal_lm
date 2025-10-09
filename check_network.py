import socket
import os
from dotenv import load_dotenv

load_dotenv()

def check_connection():
    lm_url = os.getenv('LM_STUDIO_URL', 'http://localhost:1234/v1')
    
    # Извлекаем хост и порт из URL
    if '://' in lm_url:
        host_port = lm_url.split('://')[1].split('/')[0]
        host = host_port.split(':')[0]
        port = int(host_port.split(':')[1]) if ':' in host_port else 1234
    else:
        host = 'localhost'
        port = 1234
    
    print(f"Проверяем подключение к {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print("✅ Порт открыт! Сетевое подключение есть.")
            return True
        else:
            print(f"❌ Порт закрыт. Код ошибки: {result}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    check_connection()