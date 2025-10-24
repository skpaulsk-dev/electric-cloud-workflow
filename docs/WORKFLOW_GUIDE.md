# Руководство разработчика Workflow

## Архитектура системы
Система состоит из трёх основных компонентов:
1. **Yandex Cloud Workflow** — оркестрация процессов
2. **AI-агент** — преобразование текста в команды
3. **Electric Cloud API** — хранение и обработка данных проекта

## Рабочий процесс

### 1. Входное сообщение
Пользователь отправляет сообщение в Telegram-бот.

### 2. Маршрутизация (`route`)
- Проверка на команду `/start`
- Маршрутизация на создание проекта или загрузку контекста

### 3. Создание проекта (`do_start`)
```
HTTP POST → Electric Cloud API (upsertuserandproject)
Вход: tg_user_id, username, first_name, last_name
Выход: project_id, project_name, created (true/false)
```

### 4. Загрузка контекста (`load_ctx`)
```
HTTP POST → Electric Cloud API (getcurrentproject)
Вход: tg_user_id
Выход: context (JSON с иерархией проекта), name
```

### 5. Обработка AI (`call_ai`)
- Передача текста сообщения и контекста проекту
- AI возвращает строгий JSON с командами
- Формат: `{"kind": "proj_context", "commands": [...], "confirm_needed": true}`

### 6. Применение команд (`apply_batch`)
```
HTTP POST → Electric Cloud API (applybatch)
Вход: tg_user_id, batch (JSON от AI)
Выход: applied/total счетчики, results[], rev_id
```

### 7. Ответ пользователю (`reply_*`)
Отправка результатов через Telegram-бот.

## Формат команд для AI-агента

### Структура команды
```json
{
  "cmd_type": "add|set|move|delete|replace",
  "target_type": "project|area|electrical_box",
  "link": "root|area:/Путь|area:ID",
  "target_id": "area#ID|panel#ID", // опционально, приоритетнее link
  "payload": { /* данные для операции */ }
}
```

### Примеры использования

#### Добавление области
```json
{
  "cmd_type": "add",
  "target_type": "area",
  "link": "root",
  "payload": {
    "name": "Гостиная",
    "desc": "Основная гостиная"
  }
}
```

#### Обновление проекта
```json
{
  "cmd_type": "set",
  "target_type": "project",
  "link": "root",
  "payload": {
    "name": "Кафе на набережной",
    "address": "Ялта",
    "customer": "ООО Море"
  }
}
```

#### Перемещение щита
```json
{
  "cmd_type": "move",
  "target_type": "electrical_box",
  "link": "area:/ТП1",
  "payload": {
    "name": "ЩА",
    "to": "area:/Электрощитовая"
  }
}
```

## Правила именования и ссылок

### Пути к областям (`link`)
- `root` — корень проекта
- `area:/Имя` — область по имени (через слэш для вложенности)
- `area:ID` — область по числовому ID

### Идентификаторы (`target_id`)
- `area#ID` — для операций с областями
- `panel#ID` — для операций со щитами

### Сравнение имён
- Без учёта регистра
- Игнорирование лишних пробелов
- Нормализация Unicode

## Обработка ошибок

### Таймауты и повторные попытки
- `load_ctx`: 3 повторные попытки при 504/500/STEP_INTERNAL
- `apply_batch`: 2 повторные попытки, задержка 0.5-2 сек

### Типичные ошибки
- `area-move: cannot move into its own subtree` — нельзя переместить область в её поддерево
- `panel-move: destination area not found` — область назначения не найдена
- `Validation failed` — ошибки валидации данных

### Сообщения пользователю
- При успехе: "Готово. Применено X из Y. Ревизия: Z"
- При ошибке: "Не смог применить команды. Попробуй переформулировать запрос."

## Интеграция с Yandex Cloud

### Lockbox для секретов
- Токен Telegram-бота: `lockboxPayload("e6qgs4nem0uvu1mdvu01"; "token")`

### YandexGPT модель
- URI: `gpt://b1gcs4t2ea41k8loh09o/yandexgpt/latest`
- Роль: ассистент по электротехническому проектированию

### Cloud Function URL
- `https://functions.yandexcloud.net/d4e8ta94341329251lah`
- Действия: `upsertuserandproject`, `getcurrentproject`, `applybatch`

## Разработка и модификация

### Изменение Workflow
1. Редактировать `YAML-config-Workflow.yml`
2. Валидировать по `yawl.json`
3. Загрузить в Yandex Cloud Workflow

### Модификация AI-промпта
- Обновить `role`, `goal`, `backstory` в конфиге Workflow
- Добавить новые примеры команд
- Изменить `model` или параметры

### Добавление новых команд
1. Обновить документацию команд в AI-промпте
2. Реализовать обработку в Electric Cloud API
3. Протестировать через Workflow

## Тестирование
- Все тестирование производится в Yandex Cloud Workflow
- Мониторинг через логи Workflow
- Проверка через Telegram-бот

## Производительность
- Время обработки: 10-20 сек для сложных команд
- Лимиты: 2000 записей в батче
- Рекомендации: задержки 1-3 сек между запросами