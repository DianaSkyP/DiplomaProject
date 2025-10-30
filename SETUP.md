# Инструкция по настройке и запуску

## Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка токена YouGile
```bash
# Получите токен на https://ru.yougile.com
export YOUGILE_TOKEN="your_token_here"
```

### 3. Запуск тестов
```bash
# UI тесты
python run_tests.py ui

# API тесты  
python run_tests.py api

# Все тесты
python run_tests.py all
```

## Получение токена YouGile

1. Зарегистрируйтесь на https://ru.yougile.com
2. Перейдите в настройки профиля
3. Найдите раздел "API токены"
4. Создайте новый токен
5. Скопируйте токен и установите переменную окружения

## Возможные проблемы

### Ошибка "YOUGILE_TOKEN environment variable is required"
- Убедитесь, что установили переменную окружения
- Проверьте правильность токена

### Ошибки с браузером
- Установите Chrome или Firefox
- Проверьте, что webdriver-manager может скачать драйверы

### Ошибки с Allure
- Установите Allure: https://docs.qameta.io/allure/
- Убедитесь, что Allure в PATH

## Структура тестов

- **UI тесты** - тестируют веб-интерфейс через Selenium
- **API тесты** - тестируют REST API через requests
- **Page Objects** - инкапсулируют элементы страниц
- **API Client** - инкапсулирует работу с API

## Отчеты

После запуска тестов с флагом `--report` будет создан Allure отчет:
```bash
python run_tests.py all --report
```

Отчет откроется автоматически в браузере.
