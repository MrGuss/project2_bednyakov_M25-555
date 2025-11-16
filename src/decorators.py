import time

import prompt


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
    return wrapper


def confirm_action(func):
    def wrapper(*args, **kwargs):
        confirm = prompt.string("Вы уверены, что хотите продолжить? (y/n): ")
        if confirm.lower() == 'y':
            return func(*args, **kwargs)
        else:
            print("Действие отменено.")
    return wrapper


def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {1000*(end_time - start_time):.3f} мc")
        return result
    return wrapper
