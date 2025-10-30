"""
Базовый класс для Page Object моделей
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
import allure
from typing import Optional


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self, url: str) -> None:
        """Открыть страницу по URL"""
        with allure.step(f"Открыть страницу {url}"):
            self.driver.get(url)

    def find_element(self, locator: tuple, timeout: int = 10) -> Optional[object]:
        """Найти элемент с ожиданием"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            return None

    def find_elements(self, locator: tuple, timeout: int = 10) -> list:
        """Найти элементы с ожиданием"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    def click_element(self, locator: tuple, timeout: int = 10) -> bool:
        """Кликнуть по элементу"""
        with allure.step(f"Кликнуть по элементу {locator}"):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                return True
            except TimeoutException:
                return False

    def send_keys(self, locator: tuple, text: str, timeout: int = 10) -> bool:
        """Ввести текст в поле"""
        with allure.step(f"Ввести текст '{text}' в поле {locator}"):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
                element.clear()
                element.send_keys(text)
                return True
            except TimeoutException:
                return False

    def get_text(self, locator: tuple, timeout: int = 10) -> str:
        """Получить текст элемента"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.text
        except TimeoutException:
            return ""

    def is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
        """Проверить наличие элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_visible(self, locator: tuple, timeout: int = 10) -> bool:
        """Дождаться видимости элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_page_title(self) -> str:
        """Получить заголовок страницы"""
        return self.driver.title

    def get_current_url(self) -> str:
        """Получить текущий URL"""
        return self.driver.current_url
