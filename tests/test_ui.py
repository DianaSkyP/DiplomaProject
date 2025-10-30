"""
UI тесты для YouGile
"""
import pytest
import allure
import uuid
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.test_data import test_data
from config.settings import settings


@allure.feature("UI тесты YouGile")
class TestYougileUI:
    """Класс с UI тестами для YouGile"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Настройка перед каждым тестом"""
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.projects_page = ProjectsPage(driver)

    @allure.story("Авторизация")
    @allure.title("Успешная авторизация с валидными данными")
    @allure.description("Проверка успешной авторизации с корректными email и паролем")
    def test_successful_login(self):
        """Тест успешной авторизации"""
        with allure.step("Открыть страницу авторизации"):
            self.login_page.open_login_page()

        with allure.step("Ввести валидные данные для авторизации"):
            email = settings.TEST_EMAIL
            password = settings.TEST_PASSWORD

        with allure.step("Выполнить авторизацию"):
            success = self.login_page.login(email, password)
            assert success, "Не удалось выполнить авторизацию"

        with allure.step("Проверить успешную авторизацию"):
            assert self.login_page.is_login_successful(), "Авторизация не прошла успешно"

    @allure.story("Авторизация")
    @allure.title("Авторизация с неверными данными")
    @allure.description("Проверка отображения ошибки при авторизации с неверными данными")
    def test_login_with_invalid_credentials(self):
        """Тест авторизации с неверными данными"""
        with allure.step("Открыть страницу авторизации"):
            self.login_page.open_login_page()

        with allure.step("Ввести неверные данные для авторизации"):
            email = "invalid@example.com"
            password = "wrongpassword"

        with allure.step("Выполнить авторизацию"):
            success = self.login_page.login(email, password)
            assert success, "Не удалось выполнить авторизацию"

        with allure.step("Проверить наличие сообщения об ошибке"):
            assert self.login_page.is_error_message_present(), "Сообщение об ошибке не отображается"

    @allure.story("Управление проектами")
    @allure.title("Создание нового проекта")
    @allure.description("Проверка создания нового проекта с валидными данными")
    def test_create_new_project(self):
        """Тест создания нового проекта"""
        with allure.step("Выполнить авторизацию"):
            self.login_page.open_login_page()
            self.login_page.login(settings.TEST_EMAIL, settings.TEST_PASSWORD)
            assert self.login_page.is_login_successful(), "Авторизация не прошла успешно"

        with allure.step("Открыть страницу проектов"):
            self.projects_page.open_projects_page()

        with allure.step("Создать новый проект"):
            project_title = f"Test Project {uuid.uuid4().hex[:8]}"
            project_description = "Test project description"
            success = self.projects_page.create_project(project_title, project_description)
            assert success, "Не удалось создать проект"

        with allure.step("Проверить создание проекта"):
            assert self.projects_page.find_project_by_title(project_title), "Проект не найден в списке"

    @allure.story("Управление проектами")
    @allure.title("Создание проекта с пустым названием")
    @allure.description("Проверка отображения ошибки при создании проекта с пустым названием")
    def test_create_project_with_empty_title(self):
        """Тест создания проекта с пустым названием"""
        with allure.step("Выполнить авторизацию"):
            self.login_page.open_login_page()
            self.login_page.login(settings.TEST_EMAIL, settings.TEST_PASSWORD)
            assert self.login_page.is_login_successful(), "Авторизация не прошла успешно"

        with allure.step("Открыть страницу проектов"):
            self.projects_page.open_projects_page()

        with allure.step("Попытаться создать проект с пустым названием"):
            success = self.projects_page.create_project("")
            assert success, "Не удалось выполнить попытку создания проекта"

        with allure.step("Проверить наличие сообщения об ошибке"):
            assert self.projects_page.is_error_message_present(), "Сообщение об ошибке не отображается"

    @allure.story("Управление проектами")
    @allure.title("Редактирование существующего проекта")
    @allure.description("Проверка редактирования существующего проекта")
    def test_edit_existing_project(self):
        """Тест редактирования существующего проекта"""
        with allure.step("Выполнить авторизацию"):
            self.login_page.open_login_page()
            self.login_page.login(settings.TEST_EMAIL, settings.TEST_PASSWORD)
            assert self.login_page.is_login_successful(), "Авторизация не прошла успешно"

        with allure.step("Открыть страницу проектов"):
            self.projects_page.open_projects_page()

        with allure.step("Создать тестовый проект"):
            original_title = f"Original Project {uuid.uuid4().hex[:8]}"
            success = self.projects_page.create_project(original_title)
            assert success, "Не удалось создать тестовый проект"
            assert self.projects_page.find_project_by_title(original_title), "Тестовый проект не найден"

        with allure.step("Редактировать проект"):
            new_title = f"Updated Project {uuid.uuid4().hex[:8]}"
            new_description = "Updated project description"
            success = self.projects_page.edit_project(original_title, new_title, new_description)
            assert success, "Не удалось отредактировать проект"

        with allure.step("Проверить изменения"):
            assert self.projects_page.find_project_by_title(new_title), "Обновленный проект не найден"
