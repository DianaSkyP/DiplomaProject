"""
Page Object модель для страницы проектов YouGile
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage


class ProjectsPage(BasePage):
    """Страница проектов YouGile"""

    CREATE_PROJECT_BUTTON = (By.CSS_SELECTOR, "button[data-testid='create-project']")
    PROJECT_TITLE_INPUT = (By.CSS_SELECTOR, "input[name='title']")
    PROJECT_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea[name='description']")
    SAVE_PROJECT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "button[type='button']")
    PROJECT_ITEM = (By.CSS_SELECTOR, ".project-item")
    PROJECT_TITLE = (By.CSS_SELECTOR, ".project-title")
    EDIT_PROJECT_BUTTON = (By.CSS_SELECTOR, ".edit-project")
    DELETE_PROJECT_BUTTON = (By.CSS_SELECTOR, ".delete-project")
    CONFIRM_DELETE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='confirm-delete']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = "https://ru.yougile.com/projects"

    @allure.step("Открыть страницу проектов")
    def open_projects_page(self) -> None:
        """Открыть страницу проектов"""
        self.open(self.url)

    @allure.step("Нажать кнопку создания проекта")
    def click_create_project(self) -> bool:
        """Нажать кнопку создания проекта"""
        return self.click_element(self.CREATE_PROJECT_BUTTON)

    @allure.step("Ввести название проекта: {title}")
    def enter_project_title(self, title: str) -> bool:
        """Ввести название проекта"""
        return self.send_keys(self.PROJECT_TITLE_INPUT, title)

    @allure.step("Ввести описание проекта: {description}")
    def enter_project_description(self, description: str) -> bool:
        """Ввести описание проекта"""
        return self.send_keys(self.PROJECT_DESCRIPTION_INPUT, description)

    @allure.step("Нажать кнопку сохранения проекта")
    def click_save_project(self) -> bool:
        """Нажать кнопку сохранения проекта"""
        return self.click_element(self.SAVE_PROJECT_BUTTON)

    @allure.step("Нажать кнопку отмены")
    def click_cancel(self) -> bool:
        """Нажать кнопку отмены"""
        return self.click_element(self.CANCEL_BUTTON)

    @allure.step("Создать проект с названием: {title}")
    def create_project(self, title: str, description: str = "") -> bool:
        """Создать проект"""
        if not self.click_create_project():
            return False
        if not self.enter_project_title(title):
            return False
        if description and not self.enter_project_description(description):
            return False
        return self.click_save_project()

    @allure.step("Получить список проектов")
    def get_projects_list(self) -> list:
        """Получить список проектов"""
        projects = self.find_elements(self.PROJECT_ITEM)
        return [project.text for project in projects]

    @allure.step("Найти проект по названию: {title}")
    def find_project_by_title(self, title: str) -> bool:
        """Найти проект по названию"""
        projects = self.find_elements(self.PROJECT_TITLE)
        for project in projects:
            if title in project.text:
                return True
        return False

    @allure.step("Редактировать проект: {title}")
    def edit_project(self, old_title: str, new_title: str, new_description: str = "") -> bool:
        """Редактировать проект"""
        projects = self.find_elements(self.PROJECT_ITEM)
        for project in projects:
            if old_title in project.text:
                edit_button = project.find_element(*self.EDIT_PROJECT_BUTTON)
                edit_button.click()
                break
        else:
            return False
        if not self.enter_project_title(new_title):
            return False
        if new_description and not self.enter_project_description(new_description):
            return False
        return self.click_save_project()

    @allure.step("Удалить проект: {title}")
    def delete_project(self, title: str) -> bool:
        """Удалить проект"""
        projects = self.find_elements(self.PROJECT_ITEM)
        for project in projects:
            if title in project.text:
                delete_button = project.find_element(*self.DELETE_PROJECT_BUTTON)
                delete_button.click()
                break
        else:
            return False
        return self.click_element(self.CONFIRM_DELETE_BUTTON)

    @allure.step("Получить сообщение об успехе")
    def get_success_message(self) -> str:
        """Получить сообщение об успехе"""
        return self.get_text(self.SUCCESS_MESSAGE)

    @allure.step("Получить сообщение об ошибке")
    def get_error_message(self) -> str:
        """Получить сообщение об ошибке"""
        return self.get_text(self.ERROR_MESSAGE)

    @allure.step("Проверить наличие сообщения об успехе")
    def is_success_message_present(self) -> bool:
        """Проверить наличие сообщения об успехе"""
        return self.is_element_present(self.SUCCESS_MESSAGE)

    @allure.step("Проверить наличие сообщения об ошибке")
    def is_error_message_present(self) -> bool:
        """Проверить наличие сообщения об ошибке"""
        return self.is_element_present(self.ERROR_MESSAGE)
