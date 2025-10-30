# Дипломная работа: Автоматизация тестирования YouGile

## Описание проекта

Дипломная работа по автоматизации тестирования веб-приложения **YouGile** - системы управления проектами. Проект включает в себя UI и API тесты, написанные на Python с использованием Selenium, pytest и Allure.

**Основано на финальной работе по ручному тестированию**

## Тестируемое приложение

- **Название:** YouGile
- **URL:** https://ru.yougile.com
- **Описание:** Система управления проектами с возможностью создания, редактирования и удаления проектов

## Структура проекта

```
DiplomaProject/
├── config/                 # Конфигурационные файлы
│   ├── settings.py        # Настройки приложения
│   └── test_data.py       # Тестовые данные
├── pages/                 # Page Object модели
│   ├── base_page.py       # Базовый класс для страниц
│   ├── login_page.py      # Страница авторизации
│   └── projects_page.py   # Страница проектов
├── tests/                 # Тестовые файлы
│   ├── test_ui.py         # UI тесты (5 тестов)
│   ├── test_api.py        # API тесты (5 тестов)
│   └── conftest.py        # Конфигурация pytest
├── utils/                 # Вспомогательные утилиты
│   └── api_client.py      # API клиент для YouGile
├── reports/               # Отчеты о тестировании (не в репозитории)
├── allure-results/        # Результаты Allure (не в репозитории)
├── screenshots/           # Скриншоты (не в репозитории)
├── requirements.txt       # Зависимости Python
├── run_tests.py          # Скрипт запуска тестов
└── README.md             # Документация
```

## Тестовые сценарии

### UI тесты (5 тестов)
1. **Успешная авторизация** - проверка входа с валидными данными
2. **Авторизация с неверными данными** - проверка отображения ошибки
3. **Создание нового проекта** - проверка создания проекта с валидными данными
4. **Создание проекта с пустым названием** - проверка валидации
5. **Редактирование существующего проекта** - проверка обновления проекта

### API тесты (5 тестов)
1. **Создание проекта с валидными данными** - POST /api-v2/projects
2. **Получение проекта по ID** - GET /api-v2/projects/{id}
3. **Обновление проекта** - PUT /api-v2/projects/{id}
4. **Создание проекта с пустыми данными** - проверка валидации
5. **Получение несуществующего проекта** - проверка ошибки 404

## Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/DianaSkyP/DiplomaProject.git
cd DiplomaProject
```

### 2. Установка зависимостей
```bash
# Установка Python пакетов
pip install -r requirements.txt

```

### 3. Настройка переменных окружения
```bash
# Для API тестов необходим токен YouGile
export YOUGILE_TOKEN="your_yougile_token_here"

# Опционально: настройка браузера
export BROWSER="chrome"  # или "firefox"
export HEADLESS="false"  # или "true" для headless режима
```

## Запуск тестов

### Режимы запуска

#### 1. Только UI тесты
```bash
# Через Python скрипт
python run_tests.py ui

# С генерацией отчета
python run_tests.py ui --report
```

#### 2. Только API тесты
```bash
# Через Python скрипт
python run_tests.py api

# С генерацией отчета
python run_tests.py api --report
```

#### 3. Все тесты
```bash
# Через Python скрипт
python run_tests.py all

# С генерацией отчета
python run_tests.py all --report
```

### Прямой запуск через pytest
```bash
# UI тесты
pytest tests/test_ui.py -v --alluredir=allure-results

# API тесты
pytest tests/test_api.py -v --alluredir=allure-results

# Все тесты
pytest tests/ -v --alluredir=allure-results
```

## Генерация отчетов

### Allure отчеты
```bash
# Генерация отчета
allure generate allure-results -o allure-report --clean

# Открытие отчета
allure open allure-report

```

## Проверка качества кода

### Линтеры
```bash
# Flake8
flake8 tests/ pages/ utils/ config/ --max-line-length=100

# Pylint
pylint tests/ pages/ utils/ config/ --disable=C0114,C0116

```

### Форматирование кода
```bash
# Black
black tests/ pages/ utils/ config/ --line-length=100

# isort
isort tests/ pages/ utils/ config/ --profile=black

```

## Очистка временных файлов
```bash
rm -rf allure-results allure-report screenshots reports __pycache__ .pytest_cache
```

## Технологии

- **Python 3.8+**
- **Selenium WebDriver** - для UI тестирования
- **pytest** - фреймворк для тестирования
- **Allure** - генерация отчетов
- **requests** - для API тестирования
- **Page Object Model** - паттерн для UI тестов

## Особенности реализации

- **Page Object Model** - все UI элементы вынесены в отдельные классы
- **Allure интеграция** - подробные шаги тестов с allure.step
- **Конфигурация через переменные окружения** - гибкая настройка
- **Автоматическая очистка** - тестовые данные удаляются после тестов
- **Обработка ошибок** - валидация ответов API и UI элементов
- **Скриншоты при падении** - автоматическое создание скриншотов
- **Три режима запуска** - UI, API, все тесты
- **Соответствие PEP8** - код соответствует стандартам Python

## Автор

**DianaSkyP**

## Лицензия

Этот проект создан в рамках дипломной работы по автоматизации тестирования.