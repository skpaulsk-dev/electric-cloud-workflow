# Структура проекта Electric Cloud Workflow

## Основные директории

```
electric-cloud-workflow/
├── config/                # YAML-конфигурации проекта Workflow
│   └── (сюда загрузится основной workflow YAML)
│
├── specs/                 # Хранение спецификаций (например yawl.json)
│   └── yawl.json (загружается пользователем)
│
├── docs/                  # Документация, пояснения, диаграммы и обзоры связей
│   ├── WORKFLOW_OVERVIEW.md
│   ├── INTEGRATION_API_LINKS.md
│   └── WORKFLOW_GUIDE.md
│
└── README.md              # Описание проекта
```

## Примечания
- Все тестирование и выполнение будут производиться непосредственно в **Яндекс Cloud Workflow**.
- Репозиторий предназначен для хранения конфигурационных файлов, схем и документации интеграции с API проекта **electric-cloud-api**.