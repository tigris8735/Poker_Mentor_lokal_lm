# План архитектуры

## 1. Общая архитектура системы

Poker Mentor построен по модульной микросервисной архитектуре с четким разделением ответственности между компонентами.

```mermaid
graph TB
    TG[Telegram Client] --> TB[Telegram Bot API]
    TB --> BM[Bot Main Router]
    
    BM --> HR[Handlers Router]
    BM --> SR[Services Router]
    
    HR --> SH[Start Handler]
    HR --> GH[Game Handler]
    HR --> AH[Analysis Handler]
    HR --> LH[Learning Handler]
    
    SR --> GM[Game Manager]
    SR --> AI[AIService]
    SR --> DB[Database Service]
    
    AI --> LS[LM Studio API]
    AI --> OF[Offline AI Fallback]
    
    GM --> PE[Poker Engine]
    
    DB --> SQL[SQLite Database]
    
    LS --> QW[Qwen AI Model]
    
    style AI fill:#e1f5fe
    style GM fill:#f3e5f5
    style DB fill:#e8f5e8
```

## 2. Компоненты системы

### 2.1. Core Components

#### **🤖 Bot Core (`main.py`)**
- **Назначение**: Точка входа, инициализация и координация всех компонентов
- **Технологии**: Aiogram 3.x, asyncio
- **Ответственность**:
  - Инициализация бота и диспетчера
  - Регистрация всех роутеров
  - Управление жизненным циклом приложения

#### **🎮 Game Manager (`game_manager.py`)**
- **Назначение**: Управление игровыми сессиями и состоянием
- **Ключевые классы**: `GameManager`, `GameState`
- **Ответственность**:
  - Создание и завершение игровых сессий
  - Управление игровым состоянием (стек, банк, улицы)
  - Координация действий игрока и AI

#### **🃏 Poker Engine (`poker_engine.py`)**
- **Назначение**: Логика покерной игры
- **Ключевые функции**:
  - Создание и перемешивание колоды
  - Раздача карт (префлоп, флоп, терн, ривер)
  - Форматирование карт для отображения

### 2.2. AI Components

#### **🧠 AI Service (`ai_service.py`)**
- **Назначение**: Управление взаимодействием с AI-моделью
- **Архитектура**: Фасад-паттерн для единого интерфейса
- **Функциональность**:
  - Проверка доступности LM Studio
  - Отправка запросов к AI-модели
  - Автоматическое переключение на оффлайн-режим

#### **📡 LLM Client (`llm_client.py`)**
- **Назначение**: Низкоуровневое взаимодействие с LM Studio API
- **Протокол**: HTTP REST API совместимый с OpenAI
- **Особенности**: Таймауты, обработка ошибок, повторные попытки

#### **🔄 Offline AI (`offline_ai.py`)**
- **Назначение**: Резервная система при недоступности основного AI
- **Реализация**: База предопределенных советов и анализа
- **Стратегия**: Случайный выбор из релевантных ответов

### 2.3. Data Components

#### **💾 Database Service (`database.py`)**
- **Назначение**: Управление персистентными данными
- **ORM**: SQLAlchemy с декларативными моделями
- **Модели**:
  - `User`: данные пользователей Telegram
  - `HandHistory`: история раздач для анализа

#### **👤 User Models (`user.py`)**
- **Назначение**: Определение структуры данных
- **Особенности**: Автоматические временные метки, отношения

### 2.4. Handler Components

#### **🚀 Command Handlers**
- **`start.py`**: Приветствие, регистрация, основное меню
- **`game.py`**: Управление игровым процессом
- **`analysis.py`**: Обработка AI-запросов на анализ
- **`learning.py`**: Образовательный функционал
- **`system.py`**: Системные команды и диагностика

## 3. Взаимодействие компонентов

### 3.1. Последовательность игры

```mermaid
sequenceDiagram
    participant U as User
    participant GH as GameHandler
    participant GM as GameManager
    participant PE as PokerEngine
    participant AI as AIService

    U->>GH: /game
    GH->>GM: start_game(user_id)
    GM->>PE: create_deck(), deal_cards()
    GM-->>GH: GameState
    GH-->>U: Карты и доступные действия
    
    U->>GH: /call
    GH->>GM: user_call(user_id)
    GM->>AI: _ai_action(game)
    AI-->>GM: Результат действия AI
    GM-->>GH: Обновленное состояние
    GH-->>U: Результат хода
```

### 3.2. AI-анализ раздачи

```mermaid
sequenceDiagram
    participant U as User
    participant AH as AnalysisHandler
    participant AI as AIService
    participant LS as LM Studio
    participant OF as Offline AI

    U->>AH: /analyze + описание
    AH->>AI: analyze_hand(hand_data)
    AI->>AI: check_connection()
    
    alt LM Studio доступен
        AI->>LS: HTTP POST /chat/completions
        LS-->>AI: AI-ответ
        AI-->>AH: Профессиональный анализ
    else LM Studio недоступен
        AI->>OF: analyze_hand(hand_data)
        OF-->>AI: Базовый анализ
        AI-->>AH: Оффлайн-анализ
    end
    
    AH-->>U: Результат анализа
```

## 4. Потоки данных

### 4.1. Игровые данные
```
User Input → Telegram API → Handler → GameManager → 
PokerEngine → GameState → Response Formatter → User
```

### 4.2. AI-запросы  
```
User Question → Handler → AIService → LM Studio API →
Qwen Model → Response Parser → User
```

### 4.3. Данные пользователей
```
User Activity → Handler → Database Service → 
SQLite → User Model → Statistics
```

## 5. Масштабируемость и расширяемость

### 5.1. Горизонтальное масштабирование
- Stateless дизайн обработчиков
- Внешнее хранилище сессий (Redis готово к интеграции)
- Балансировка нагрузки между инстансами бота

### 5.2. Расширение функциональности
- Модульная система обработчиков
- Плагинная архитектура AI-провайдеров
- Легкое добавление новых игровых режимов

---

*Документация подготовлена: Шелков Данила (@dedyretti)*
