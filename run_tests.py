#!/usr/bin/env python3
"""
Скрипт для запуска тестов в разных режимах
"""
import sys
import subprocess
import argparse


def run_command(command):
    """Выполнить команду и вернуть результат"""
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e}")
        print(f"Stderr: {e.stderr}")
        return False


def run_ui_tests():
    """Запустить только UI тесты"""
    print("Запуск UI тестов...")
    command = "pytest tests/test_ui.py -v --alluredir=allure-results"
    return run_command(command)


def run_api_tests():
    """Запустить только API тесты"""
    print("Запуск API тестов...")
    command = "pytest tests/test_api.py -v --alluredir=allure-results"
    return run_command(command)


def run_all_tests():
    """Запустить все тесты"""
    print("Запуск всех тестов...")
    command = "pytest tests/ -v --alluredir=allure-results"
    return run_command(command)


def generate_allure_report():
    """Сгенерировать Allure отчет"""
    print("Генерация Allure отчета...")
    command = "allure generate allure-results -o allure-report --clean"
    return run_command(command)


def open_allure_report():
    """Открыть Allure отчет"""
    print("Открытие Allure отчета...")
    command = "allure open allure-report"
    return run_command(command)


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description="Запуск тестов YouGile")
    parser.add_argument(
        "mode",
        choices=["ui", "api", "all"],
        help="Режим запуска: ui (только UI), api (только API), all (все)"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Сгенерировать и открыть Allure отчет"
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Открыть существующий Allure отчет"
    )

    args = parser.parse_args()

    # Проверка наличия токена для API тестов
    if args.mode in ["api", "all"]:
        import os
        if not os.getenv("YOUGILE_TOKEN"):
            print("Ошибка: Не установлен YOUGILE_TOKEN")
            print("Установите токен: export YOUGILE_TOKEN=your_token_here")
            sys.exit(1)

    # Запуск тестов
    success = False
    if args.mode == "ui":
        success = run_ui_tests()
    elif args.mode == "api":
        success = run_api_tests()
    elif args.mode == "all":
        success = run_all_tests()

    if not success:
        print("Тесты завершились с ошибками")
        sys.exit(1)

    print("Тесты выполнены успешно")

    # Генерация и открытие отчета
    if args.report:
        if generate_allure_report():
            open_allure_report()
    elif args.open:
        open_allure_report()


if __name__ == "__main__":
    main()
