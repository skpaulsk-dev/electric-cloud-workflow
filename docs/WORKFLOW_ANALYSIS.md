# Анализ Workflow и спецификации YAWL

## Обзор Workflow
Workflow в проекте представляет собой цепочку шагов для обработки Telegram-сообщений с использованием AI-агента и интеграции с **Electric Cloud API**.

### Структура Workflow
- **Версия YAWL**: 0.1
- **Начальный шаг**: `route`
- **Шаги**:
  - `route`: Маршрутизация на основе текста сообщения (`/start` или другие)
  - `do_start`: Создание/поиск проекта через API
  - `load_ctx`: Загрузка контекста проекта
  - `call_ai`: Вызов AI-агента для преобразования запроса в команды
  - `reply_ai`: Отправка ответа пользователя
  - `apply_batch`: Применение команд через API
  - `reply_apply`: Сообщение результатов применения

### Входы и выходы
- **Вход**: Telegram-сообщение с текстом, ID пользователя и чата
- **Выход**: Сообщения в Telegram-чат с результатами обработки

### Ключевые компоненты
1. **Telegram-бот**: Отправка сообщений пользователю
2. **HTTP-вызовы**: Интеграция с Cloud Function (Electric Cloud API)
3. **AI-агент**: Преобразование текста в структурированные команды

## Спецификация YAWL.json
Файл содержит полную схему JSON для валидации YAWL Workflow версии 0.1.

### Основные элементы
- `Workflow`: Корневой объект с версией, стартом и шагами
- `Step`: Шаги могут быть различных типов (switch, httpCall, aiAgent, telegramBot и др.)
- `AIAgent`: Конфигурация AI-агента с ролью, целью, бэкстори и моделью
- `HTTPCall`: HTTP-запросы к внешним сервисам
- `TelegramBot`: Интеграция с Telegram

### Допустимые команды для AI-агента
- `cmd_type`: add | move | replace | delete | set
- `target_type`: project | area | electrical_box | product
- `link`: Пути к сущностям (root, area:/Путь, area:ID, panel:<id|name>)
- `target_id`: Идентификаторы для операций (area#ID, panel#ID)
- `payload`: Данные для создания/обновления

## Взаимосвязи с Electric Cloud API
Workflow взаимодействует с **electric-cloud-api** через HTTP-вызовы к Cloud Function:

- `https://functions.yandexcloud.net/d4e8ta94341329251lah`
- Действия: `upsertuserandproject`, `getcurrentproject`, `applybatch`

### Форматы данных
- Вход/выход: JSON с ключами `tg_user_id`, `tg_username`, `first_name`, etc.
- Команды батча: Массив объектов с `cmd_type`, `target_type`, `link`, `payload`
- Результаты: Сведения о применённых изменениях, ошибках и ревизиях

## Рекомендации по структуре проекта
На основе анализа рекомендую организовать файлы следующим образом:
- `config/workflow.yml` — основной файл конфигурации
- `specs/yawl.json` — спецификация схемы
- `docs/` — документация интеграции и разработки