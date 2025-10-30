"""
API тесты для YouGile
"""
import pytest
import allure
import uuid
from utils.api_client import YougileAPIClient


@allure.feature("API тесты YouGile")
class TestYougileAPI:
    """Класс с API тестами для YouGile"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Настройка перед каждым тестом"""
        self.api_client = YougileAPIClient()

    @pytest.fixture
    def test_project_data(self):
        """Тестовые данные для проекта"""
        unique_name = f"Test Project {uuid.uuid4().hex[:8]}"
        return {
            "title": unique_name
        }

    @pytest.fixture
    def created_project(self, test_project_data):
        """Создать проект для тестирования"""
        with allure.step("Создать тестовый проект"):
            response = self.api_client.create_project(test_project_data)
            assert self.api_client.is_successful_response(response, [201]), (
                f"Failed to create project: {response.status_code}. "
                f"Error: {self.api_client.get_error_message(response)}"
            )

        project_data = response.json()
        project_id = project_data["id"]

        yield {
            "id": project_id,
            "data": project_data,
            "original_request": test_project_data
        }

        with allure.step("Удалить тестовый проект"):
            cleanup_response = self.api_client.delete_project(project_id)
            valid_codes = [200, 204, 404]
            cleanup_msg = (f"Failed to cleanup project {project_id}: "
                          f"{cleanup_response.status_code}")
            assert cleanup_response.status_code in valid_codes, cleanup_msg

    @allure.story("Управление проектами")
    @allure.title("Создание проекта с валидными данными")
    @allure.description("Проверка создания проекта с корректными данными")
    def test_create_project_positive(self, test_project_data):
        """Тест создания проекта с валидными данными"""
        with allure.step("Создать проект"):
            response = self.api_client.create_project(test_project_data)

        with allure.step("Проверить успешность создания"):
            expected_code = 201
            actual_code = response.status_code
            error_msg = self.api_client.get_error_message(response)
        success = self.api_client.is_successful_response(response, [expected_code])
        error_text = (f"Expected {expected_code}, got {actual_code}. "
                      f"Error: {error_msg}")
        assert success, error_text

        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            has_id = "id" in response_data
            assert has_id, "Response should contain project ID"
            id_is_string = isinstance(response_data["id"], str)
            assert id_is_string, "Project ID should be string"
            id_not_empty = response_data["id"]
            assert id_not_empty, "Project ID should not be empty"

        with allure.step("Очистить созданный проект"):
            project_id = response_data["id"]
            cleanup_response = self.api_client.delete_project(project_id)
            valid_codes = [200, 204, 404]
        assert cleanup_response.status_code in valid_codes

    @allure.story("Управление проектами")
    @allure.title("Получение проекта по ID")
    @allure.description("Проверка получения существующего проекта по ID")
    def test_get_project_positive(self, created_project):
        """Тест получения проекта по ID"""
        project_id = created_project["id"]

        with allure.step("Получить проект по ID"):
            response = self.api_client.get_project(project_id)

        with allure.step("Проверить успешность получения"):
            expected_code = 200
            actual_code = response.status_code
            error_msg = self.api_client.get_error_message(response)
        success = self.api_client.is_successful_response(response, [expected_code])
        error_text = (f"Expected {expected_code}, got {actual_code}. "
                      f"Error: {error_msg}")
        assert success, error_text

        with allure.step("Проверить корректность данных"):
            response_data = response.json()
            project_id_match = response_data["id"] == project_id
        assert project_id_match, "Project ID mismatch"

    @allure.story("Управление проектами")
    @allure.title("Обновление проекта")
    @allure.description("Проверка обновления существующего проекта")
    def test_update_project_positive(self, created_project):
        """Тест обновления проекта"""
        project_id = created_project["id"]
        updated_data = {
            "title": f"Updated Test Project {uuid.uuid4().hex[:8]}"
        }

        with allure.step("Обновить проект"):
            response = self.api_client.update_project(project_id, updated_data)

        with allure.step("Проверить успешность обновления"):
            expected_code = 200
            actual_code = response.status_code
            error_msg = self.api_client.get_error_message(response)
        success = self.api_client.is_successful_response(response, [expected_code])
        error_text = (f"Expected {expected_code}, got {actual_code}. "
                      f"Error: {error_msg}")
        assert success, error_text

        with allure.step("Проверить корректность обновления"):
            response_data = response.json()
            project_id_match = response_data["id"] == project_id
        assert project_id_match, "Project ID mismatch"

    @allure.story("Управление проектами")
    @allure.title("Создание проекта с пустыми данными")
    @allure.description("Проверка ошибки при создании проекта с пустыми данными")
    def test_create_project_negative_empty_data(self):
        """Тест создания проекта с пустыми данными"""
        invalid_data = {}

        with allure.step("Попытаться создать проект с пустыми данными"):
            response = self.api_client.create_project(invalid_data)

        with allure.step("Проверить ошибку валидации"):
            expected_codes = [400, 422]
            actual_code = response.status_code
            error_msg = self.api_client.get_error_message(response)
            success = self.api_client.is_successful_response(response, expected_codes)
            error_text = (f"Expected {expected_codes} for empty data, "
                          f"got {actual_code}. Error: {error_msg}")
            assert success, error_text

    @allure.story("Управление проектами")
    @allure.title("Получение несуществующего проекта")
    @allure.description("Проверка ошибки при получении несуществующего проекта")
    def test_get_project_negative_nonexistent_id(self):
        """Тест получения несуществующего проекта"""
        nonexistent_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

        with allure.step("Попытаться получить несуществующий проект"):
            response = self.api_client.get_project(nonexistent_id)

        with allure.step("Проверить ошибку 404"):
            expected_code = 404
            actual_code = response.status_code
            error_msg = self.api_client.get_error_message(response)
            success = self.api_client.is_successful_response(response, [expected_code])
            error_text = (f"Expected {expected_code} for nonexistent project, "
                          f"got {actual_code}. Error: {error_msg}")
            assert success, error_text
