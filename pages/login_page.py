"""
Page Object модель для страницы авторизации YouGile
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage


class LoginPage(BasePage):
    """Страница авторизации YouGile"""

    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Забыли пароль?")
    REGISTER_LINK = (By.LINK_TEXT, "Регистрация")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = "https://ru.yougile.com/login"

    @allure.step("Открыть страницу авторизации")
    def open_login_page(self) -> None:
        """Открыть страницу авторизации"""
        self.open(self.url)

    @allure.step("Ввести email: {email}")
    def enter_email(self, email: str) -> bool:
        """Ввести email"""
        return self.send_keys(self.EMAIL_INPUT, email)

    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> bool:
        """Ввести пароль"""
        return self.send_keys(self.PASSWORD_INPUT, password)

    @allure.step("Нажать кнопку входа")
    def click_login_button(self) -> bool:
        """Нажать кнопку входа"""
        return self.click_element(self.LOGIN_BUTTON)

    @allure.step("Выполнить авторизацию с email: {email}")
    def login(self, email: str, password: str) -> bool:
        """Выполнить полную авторизацию"""
        self.open_login_page()
        if not self.enter_email(email):
            return False
        if not self.enter_password(password):
            return False
        return self.click_login_button()

    @allure.step("Получить сообщение об ошибке")
    def get_error_message(self) -> str:
        """Получить сообщение об ошибке"""
        return self.get_text(self.ERROR_MESSAGE)

    @allure.step("Проверить наличие сообщения об ошибке")
    def is_error_message_present(self) -> bool:
        """Проверить наличие сообщения об ошибке"""
        return self.is_element_present(self.ERROR_MESSAGE)

    @allure.step("Проверить успешную авторизацию")
    def is_login_successful(self) -> bool:
        """Проверить успешную авторизацию"""
        return "login" not in self.get_current_url().lower()

    @allure.step("Нажать ссылку 'Забыли пароль?'")
    def click_forgot_password(self) -> bool:
        """Нажать ссылку 'Забыли пароль?'"""
        return self.click_element(self.FORGOT_PASSWORD_LINK)

    @allure.step("Нажать ссылку 'Регистрация'")
    def click_register_link(self) -> bool:
        """Нажать ссылку 'Регистрация'"""
        return self.click_element(self.REGISTER_LINK)
