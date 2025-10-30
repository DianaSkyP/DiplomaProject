"""
Тестовые данные для автоматизации тестирования
"""
from typing import Dict, List, Any


class TestData:
    """Класс с тестовыми данными"""

    # Пользователи для тестирования
    USERS = {
        "valid_user": {
            "email": "test@example.com",
            "password": "password123",
            "username": "testuser"
        },
        "admin_user": {
            "email": "admin@example.com", 
            "password": "admin123",
            "username": "admin"
        }
    }

    # API endpoints
    API_ENDPOINTS = {
        "projects": "/api-v2/projects",
        "project_by_id": "/api-v2/projects/{project_id}",
        "login": "/api/auth/login",
        "register": "/api/auth/register"
    }

    # Тестовые данные для проектов
    PROJECT_DATA = {
        "valid_project": {
            "title": "Test Project"
        },
        "project_with_description": {
            "title": "Test Project with Description",
            "description": "This is a test project description"
        },
        "invalid_project": {
            "title": ""
        },
        "empty_project": {}
    }

    # Ожидаемые сообщения
    MESSAGES = {
        "success_login": "Добро пожаловать!",
        "error_invalid_credentials": "Неверный логин или пароль",
        "success_project_created": "Проект создан",
        "error_required_field": "Это поле обязательно",
        "error_project_not_found": "Проект не найден"
    }

    # Селекторы для UI тестов YouGile
    SELECTORS = {
        "login_form": {
            "email_input": "input[name='email']",
            "password_input": "input[name='password']",
            "submit_button": "button[type='submit']",
            "error_message": ".error-message"
        },
        "project_form": {
            "title_input": "input[name='title']",
            "description_input": "textarea[name='description']",
            "create_button": "button[type='submit']",
            "cancel_button": "button[type='button']"
        },
        "project_list": {
            "project_item": ".project-item",
            "project_title": ".project-title",
            "edit_button": ".edit-project",
            "delete_button": ".delete-project"
        }
    }


# Экземпляр тестовых данных
test_data = TestData()
