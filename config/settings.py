"""
Конфигурационные настройки для автоматизации тестирования
"""
import os
from typing import Optional


class Settings:
    """Настройки приложения для тестирования"""

    # Базовые URL
    BASE_URL: str = os.getenv("BASE_URL", "https://ru.yougile.com")
    API_URL: str = os.getenv("API_URL", "https://ru.yougile.com/api-v2")

    # Настройки браузера
    BROWSER: str = os.getenv("BROWSER", "chrome")
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    WINDOW_SIZE: tuple = (1920, 1080)

    # Таймауты
    IMPLICIT_WAIT: int = 10
    EXPLICIT_WAIT: int = 20
    PAGE_LOAD_TIMEOUT: int = 30

    # Тестовые данные
    TEST_EMAIL: str = os.getenv("TEST_EMAIL", "test@example.com")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", "password123")

    # API настройки
    API_TOKEN: Optional[str] = os.getenv("YOUGILE_TOKEN")
    API_TIMEOUT: int = 30

    # Пути к файлам
    SCREENSHOTS_DIR: str = "screenshots"
    REPORTS_DIR: str = "reports"
    ALLURE_RESULTS_DIR: str = "allure-results"


# Экземпляр настроек
settings = Settings()
