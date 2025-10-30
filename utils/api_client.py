"""
API клиент для YouGile
"""
import requests
import os
from typing import Dict, Any, Optional, List
import allure
from config.settings import settings


class YougileAPIClient:
    """API клиент для работы с YouGile"""

    def __init__(self):
        self.base_url = settings.API_URL
        self.token = settings.API_TOKEN
        if not self.token:
            raise ValueError(
                "YOUGILE_TOKEN environment variable is required. "
                "Please set it with your API token from yougile.com"
            )

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.timeout = settings.API_TIMEOUT

    def _make_request(self, method: str, endpoint: str, 
                      data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Выполнить HTTP запрос"""
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                return self.session.get(url)
            elif method.upper() == "POST":
                return self.session.post(url, json=data)
            elif method.upper() == "PUT":
                return self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                return self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")

    def _validate_project_data(self, project_data: Dict[str, Any]) -> None:
        """Валидация данных проекта"""
        if not isinstance(project_data, dict):
            raise ValueError("Project data must be a dictionary")

    def _validate_project_id(self, project_id: str) -> None:
        """Валидация ID проекта"""
        if not project_id or not isinstance(project_id, str):
            raise ValueError("Project ID must be a non-empty string")

    @allure.step("Проверить успешность ответа")
    def is_successful_response(self, response: requests.Response, 
                              expected_codes: List[int]) -> bool:
        """Проверить успешность ответа"""
        return response.status_code in expected_codes

    @allure.step("Получить сообщение об ошибке")
    def get_error_message(self, response: requests.Response) -> str:
        """Получить сообщение об ошибке"""
        try:
            error_data = response.json()
            return error_data.get("message", f"HTTP {response.status_code}")
        except Exception:
            return f"HTTP {response.status_code}: {response.text}"

    @allure.step("Создать проект: {project_data}")
    def create_project(self, project_data: Dict[str, Any]) -> requests.Response:
        """Создать проект"""
        self._validate_project_data(project_data)
        return self._make_request("POST", "/projects", project_data)

    @allure.step("Получить проект по ID: {project_id}")
    def get_project(self, project_id: str) -> requests.Response:
        """Получить проект по ID"""
        self._validate_project_id(project_id)
        return self._make_request("GET", f"/projects/{project_id}")

    @allure.step("Обновить проект {project_id}")
    def update_project(self, project_id: str, 
                      project_data: Dict[str, Any]) -> requests.Response:
        """Обновить проект"""
        self._validate_project_id(project_id)
        self._validate_project_data(project_data)
        return self._make_request("PUT", f"/projects/{project_id}", project_data)

    @allure.step("Удалить проект: {project_id}")
    def delete_project(self, project_id: str) -> requests.Response:
        """Удалить проект"""
        self._validate_project_id(project_id)
        return self._make_request("DELETE", f"/projects/{project_id}")

    @allure.step("Получить все проекты")
    def get_all_projects(self) -> requests.Response:
        """Получить все проекты"""
        return self._make_request("GET", "/projects")

    @allure.step("Создать проект и получить ID")
    def create_project_and_get_id(self, project_data: Dict[str, Any]) -> str:
        """Создать проект и получить ID"""
        response = self.create_project(project_data)
        if not self.is_successful_response(response, [201]):
            error_msg = self.get_error_message(response)
            raise Exception(f"Failed to create project: {error_msg}")
        return response.json()["id"]

    @allure.step("Проверить существование проекта: {project_id}")
    def project_exists(self, project_id: str) -> bool:
        """Проверить существование проекта"""
        try:
            response = self.get_project(project_id)
            return self.is_successful_response(response, [200])
        except Exception:
            return False

    @allure.step("Ожидать удаления проекта: {project_id}")
    def wait_for_project_deletion(self, project_id: str, 
                                 max_attempts: int = 3) -> bool:
        """Ожидать удаления проекта"""
        import time

        for _ in range(max_attempts):
            if not self.project_exists(project_id):
                return True
            time.sleep(1)

        return False
