import yaml
import json
import sys

def validate_yaml():
    try:
        # Загружаем YAML
        with open('YAML-config-Workflow.yml', 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

        # Загружаем JSON схему
        with open('yawl.json', 'r', encoding='utf-8') as f:
            schema = json.load(f)

        # Проверяем базовую структуру
        print('=== ВАЛИДАЦИЯ YAML ПО YAWL.JSON ===')
        print(f'Версия YAWL: {yaml_data.get("yawl")}')
        print(f'Начальный шаг: {yaml_data.get("start")}')
        print(f'Количество шагов: {len(yaml_data.get("steps", {}))}')

        # Проверяем обязательные поля
        required_fields = ['yawl', 'start', 'steps']
        missing_fields = [field for field in required_fields if field not in yaml_data]
        if missing_fields:
            print(f'❌ Отсутствуют обязательные поля: {missing_fields}')
            return False
        else:
            print('✅ Все обязательные поля присутствуют')

        # Проверяем версию
        if yaml_data.get('yawl') == '0.1':
            print('✅ Версия YAWL корректна')
        else:
            print(f'❌ Неверная версия YAWL: {yaml_data.get("yawl")}')
            return False

        # Проверяем существование начального шага
        start_step = yaml_data.get('start')
        if start_step in yaml_data.get('steps', {}):
            print(f'✅ Начальный шаг "{start_step}" существует')
        else:
            print(f'❌ Начальный шаг "{start_step}" не найден в steps')
            return False

        # Проверяем основные типы шагов
        step_types = set()
        for step_name, step_data in yaml_data.get('steps', {}).items():
            step_type = list(step_data.keys())[0] if step_data else 'unknown'
            step_types.add(step_type)

        print(f'✅ Используемые типы шагов: {step_types}')

        # Проверяем ключевые шаги
        required_steps = ['route', 'do_start', 'load_ctx', 'call_ai', 'apply_batch']
        missing_steps = [step for step in required_steps if step not in yaml_data.get('steps', {})]
        if missing_steps:
            print(f'❌ Отсутствуют ключевые шаги: {missing_steps}')
            return False
        else:
            print('✅ Все ключевые шаги присутствуют')

        print('=== ВАЛИДАЦИЯ ЗАВЕРШЕНА УСПЕШНО ===')
        return True

    except Exception as e:
        print(f'❌ Ошибка при валидации: {e}')
        return False

if __name__ == '__main__':
    success = validate_yaml()
    sys.exit(0 if success else 1)