import time
import functools


def handle_db_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: {e}")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper


def confirm_action(action_name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                answer = input(
                    f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
                ).strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                print("Операция отменена.")
                return None

            if answer != "y":
                print("Операция отменена.")
                return None

            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            result = func(*args, **kwargs)
            elapsed = time.monotonic() - start
            print(
                f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд")
            return result
        return wrapper
    return decorator


def create_cacher():
    def cache_result(key, value_func):
        pass
    return cache_result
