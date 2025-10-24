# Интеграция Workflow с Electric Cloud API

## Обзор архитектуры
Проект **electric-cloud-workflow** взаимодействует с **electric-cloud-api** через Yandex Cloud Function, которая предоставляет API для управления контекстом электротехнических проектов.

## Ключевые эндпоинты API

### 1. Создание/поиск проекта (`upsertuserandproject`)
**URL:** `https://functions.yandexcloud.net/d4e8ta94341329251lah`

**Входные данные (Workflow):**
```json
{
  "action": "upsertuserandproject",
  "tg_user_id": 123456789,
  "tg_username": "user123",
  "first_name": "Иван",
  "last_name": "Иванов",
  "language_code": "ru"
}
```

**Выходные данные:**
```json
{
  "created": true, // или false если проект уже существует
  "project_name": "Проект Ивана",
  "project_id": 42
}
```

### 2. Получение контекста проекта (`getcurrentproject`)
**URL:** `https://functions.yandexcloud.net/d4e8ta94341329251lah`

**Входные данные:**
```json
{
  "action": "getcurrentproject",
  "tg_user_id": 123456789
}
```

**Выходные данные:**
```json
{
  "context": {
    "id": 42,
    "name": "Проект Ивана",
    "description": "Описание проекта",
    "address": "Адрес объекта",
    "customer": "Заказчик",
    "areas": [
      {
        "id": 1,
        "name": "Гостиная",
        "desc": "Основная гостиная",
        "areas": [],
        "electrical_boxes": []
      }
    ],
    "electrical_boxes": []
  },
  "name": "Проект Ивана"
}
```

### 3. Применение батча команд (`applybatch`)
**URL:** `https://functions.yandexcloud.net/d4e8ta94341329251lah`

**Входные данные:**
```json
{
  "action": "applybatch",
  "tg_user_id": 123456789,
  "batch": {
    "kind": "proj_context",
    "confirm_needed": true,
    "description": "Добавление области",
    "commands": [
      {
        "cmd_type": "add",
        "target_type": "area",
        "link": "root",
        "payload": {
          "name": "Кухня"
        }
      }
    ]
  }
}
```

**Выходные данные:**
```json
{
  "applied": 1,
  "total": 1,
  "results": [
    {
      "ok": true,
      "index": 0
    }
  ],
  "rev_id": 123
}
```

## Структура данных проекта

### Иерархия контекста
```
project (корень)
├── метаданные (name, description, address, customer)
├── areas[] (области/помещения)
│   ├── areas[] (вложенные области)
│   └── electrical_boxes[] (электрощиты)
└── electrical_boxes[] (щиты верхнего уровня)
```

### Типы команд
- `add` — добавление сущностей
- `set` — обновление полей
- `move` — перемещение сущностей
- `delete` — удаление
- `replace` — замена

### Типы целей (`target_type`)
- `project` — метаданные проекта
- `area` — области/помещения
- `electrical_box` — электрощиты

## Сопоставление с Workflow
1. **Входное сообщение Telegram** → маршрутизация (`route`)
2. **Создание проекта** (`do_start`) → API `upsertuserandproject`
3. **Загрузка контекста** (`load_ctx`) → API `getcurrentproject`
4. **AI-агент** (`call_ai`) → преобразование текста в команды
5. **Применение команд** (`apply_batch`) → API `applybatch`
6. **Ответ пользователю** (`reply_*`) → Telegram-бот

## Обработка ошибок
- Таймауты: retry политики в Workflow (до 3 попыток)
- HTTP ошибки: 500/504 — повторные попытки
- Ошибки API: обработка в шагах `reply_backend_error`, `reply_ai_error`

## Производительность
- API поддерживает 5000-10000 записей/сек
- Рекомендуемые задержки между запросами: 1-3 сек
- Максимальный размер батча: 2000 записей

## Безопасность
- Все запросы содержат `tg_user_id` для идентификации пользователя
- Доступ через Yandex Cloud Function с аутентификацией
- Токены Telegram-бота хранятся в Lockbox