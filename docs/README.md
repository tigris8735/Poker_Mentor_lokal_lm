# 🃏 Poker Mentor - AI-Powered Poker Coaching Bot

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)
![LM Studio](https://img.shields.io/badge/LM_Studio-AI_Integration-orange.svg)

**Telegram бот с интеграцией ИИ-ассистента для обучения игре в покер**

## 📋 О проекте

Poker Mentor - это инновационный Telegram бот, сочетающий в себе игровую платформу для тренировки покера и интеллектуального AI-помощника на базе LM Studio с моделью Qwen. Проект предоставляет уникальную возможность изучать и совершенствовать покерные навыки через интерактивное взаимодействие.

## 🚀 Основные возможности

- 🎮 **Интерактивная игра в покер** с AI-оппонентом
- 🤖 **AI-анализ раздач** с профессиональными рекомендациями
- 📚 **Персонализированные советы** по игровым ситуациям
- 💾 **История игр** и отслеживание прогресса
- 🔄 **Гибкая архитектура** с оффлайн-режимом

## 🏗 Архитектура

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Telegram API  │◄──►│   Poker Mentor   │◄──►│   LM Studio     │
│                 │    │     Bot Core     │    │    (Qwen AI)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │   SQLite DB     │
                        │   (Users/Stats) │
                        └─────────────────┘
```

## ⚡ Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/tigris8735/Poker_Mentor.git
cd Poker_Mentor

# Установка зависимостей
pip install -r requirements.txt

# Настройка окружения
cp .env.example .env
# Заполните BOT_TOKEN в .env файле

# Запуск бота
python main.py
```

## 📖 Документация

Полная документация проекта доступна в папке [docs/](./docs/):

- [Бизнес-требования](https://github.com/tigris8735/Poker_Mentor_lokal_lm/blob/main/docs/01-business-requirements.md)
- [Системный анализ](https://github.com/tigris8735/Poker_Mentor_lokal_lm/blob/main/docs/02-system-analysis.md)
- [План архитектуры](https://github.com/tigris8735/Poker_Mentor_lokal_lm/blob/main/docs/03-architecture-plan.md)
- [Техническое задание](https://github.com/tigris8735/Poker_Mentor_lokal_lm/blob/main/docs/04-technical-specification.md)
- [План тестирования](https://github.com/tigris8735/Poker_Mentor_lokal_lm/blob/main/docs/05-testing-plan.md)
- [Отчет о приемке](https://github.com/tigris8735/Poker_Mentor_lokal_lm/blob/main/docs/06-project-acceptance-report.md)

## 🛠 Технологический стек

- **Backend**: Python 3.8+
- **Telegram Bot**: Aiogram 3.x
- **AI Integration**: LM Studio + Qwen模型
- **Database**: SQLite + SQLAlchemy
- **Architecture**: Async/await, Modular Design

## 👥 Команда разработки

| Роль | Разработчик | GitHub |
|------|-------------|---------|
| Team Lead & Backend | Чернаков Денис | [@tigris8735](https://github.com/tigris8735) |
| Backend Developer | Татаринов Вячеслав | [@shinsetsuwhy](https://github.com/shinsetsuwhy) |
| Technical Writer | Шелков Данила | [@dedyretti](https://github.com/dedyretti) |

---

*Документация подготовлена: Шелков Данила (@dedyretti)*

---
