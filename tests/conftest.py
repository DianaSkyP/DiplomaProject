"""
Конфигурация pytest для автоматизации тестирования
"""
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.settings import settings


@pytest.fixture(scope="session")
def browser_config():
    """Конфигурация браузера для тестов"""
    return {
        "browser": settings.BROWSER,
        "headless": settings.HEADLESS,
        "window_size": settings.WINDOW_SIZE
    }


@pytest.fixture(scope="function")
def driver(browser_config):
    """Фикстура для создания драйвера браузера"""
    browser = browser_config["browser"].lower()

    if browser == "chrome":
        options = ChromeOptions()
        if browser_config["headless"]:
            options.add_argument("--headless")
        w, h = browser_config['window_size']
        window_size = f"{w},{h}"
        options.add_argument(f"--window-size={window_size}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if browser_config["headless"]:
            options.add_argument("--headless")
        width = browser_config['window_size'][0]
        height = browser_config['window_size'][1]
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")

        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser}")

    # Настройка таймаутов
    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def api_client():
    """Фикстура для API клиента"""
    import requests

    session = requests.Session()
    session.timeout = settings.API_TIMEOUT

    if settings.API_TOKEN:
        auth_header = f"Bearer {settings.API_TOKEN}"
        session.headers.update({"Authorization": auth_header})

    return session


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Получаем драйвер из фикстуры
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            try:
                screenshot_dir = settings.SCREENSHOTS_DIR
                screenshot_path = f"{screenshot_dir}/failed_{item.name}.png"
                driver.save_screenshot(screenshot_path)
                allure.attach.file(
                    screenshot_path,
                    name="Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Не удалось создать скриншот: {e}")


def pytest_configure(config):
    """Конфигурация pytest"""
    import os
    os.makedirs(settings.SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    os.makedirs(settings.ALLURE_RESULTS_DIR, exist_ok=True)
