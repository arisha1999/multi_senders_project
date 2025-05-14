# Multi Senders Project

**Multi Senders** — это универсальная платформа для отправки уведомлений (SMS, email, звонки) через различные сервисы, с возможностью создания собственных чат-ботов и мультиадминки.

## 🚀 Возможности

* Поддержка нескольких провайдеров:

  * **SMS**: Twilio, Infobip, MessageBird, SMS.ru, P1SMS, Nexmo, Mobizon
  * **Email**: через SMTP
  * **Звонки**: Twilio, Infobip, Zvonobot
* Единый API-интерфейс
* Гибкое логирование через Grafana Loki
* Расширяемая архитектура
* Планируемая поддержка чат-ботов и мультиадминки

## 🧱 Структура проекта

```
multi_senders_project/
├── app/
│   ├── utils/             # Утилиты
│   ├── configs/           # Конфигурации, логгеры, 
│   ├── routers/           # FastAPI endpoints
│   ├── models/            # Pydantic-схемы
│   ├── classes/           # Модули отправки по провайдерам
│   └── main.py            # Точка входа в приложение
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🐳 Быстрый старт с Docker

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/arisha1999/multi_senders_project.git
cd multi_senders_project
```

### 2. Создайте `.env` файл

Пример `.env`:

```env
# Loki
LOKI_URL=http://localhost:3100
```

### 3. Запустите через Docker Compose

```bash
docker-compose up --build
```

Swagger будет доступен по адресу: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📌 Планы

* [ ] Интерфейс мультиадминки
* [ ] UI для построения чат-ботов
* [ ] Хранилище шаблонов
* [ ] Поддержка сценариев отправки (цепочки)
* [ ] Авторизация

## 📬 Обратная связь

Автор: [@physicist\_liketotravel](https://t.me/physicist_liketotravel)
GitHub: [arisha1999](https://github.com/arisha1999)
