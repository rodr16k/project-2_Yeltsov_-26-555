import json
import os
import prompt


commands = {
    'create_tables <имя_таблицы> <столбец1:тип> <столбец2:тип>': 'создать таблицу',
    'list_tables': 'показать таблицы',
    'drop_tables <имя_таблицы>': 'удалить таблицу',
    'exit': 'выйти из программы',
    'help': 'справочная информация'
}


def save_metadata(filepath, data):
    """ Сохраняет структуру БД в json-файл."""

    try:
        dir_name = os.path.dirname(filepath)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return True
    except Exception as e:
        print(f"При сохранении базы данных произошла ошибка: {e}")
        return False


def load_metadata(filepath):
    """ 
    Загружает структуру БД из json-файла.
    Если файла нет, возвращает пустой словарь.
    """

    try:
        with open(filepath, 'r', encoding='utf=8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.\nСоздается новая база данных.")
        return {}
    except json.JSONDecodeError:
        print("Файл содержит некорректный JSON-код.")
        return {}


def parse_user_input(user_input: str) -> tuple:
    """ Разбирает ввод пользователя на команды и аргументы."""

    user_input_list = user_input.strip().split()

    if not user_input_list:
        return ("unknown", None)

    command = user_input_list[0]

    if command == 'create_table':

        if len(user_input_list) < 3:
            print("Недостаточно аргументов для создания таблицы")
            return ('unknown', None)

        table_name = user_input_list[1]
        columns = {}

        for col in user_input_list[2:]:
            if ':' not in col:
                print('Неверный формат столбцов. Ожидается: <name:type>')

            col_name, col_type = col.split(':', 1)
            columns[col_name] = col_type

        return (command, table_name, columns)

    if command == 'list_tables':
        return (command,)

    if command == 'drop_table':

        if len(user_input_list) < 2:
            print("Укажите имя таблицы для удаления")
            return ('unknown', None)
        drop_name = user_input_list[1]
        return (command, drop_name)

    if command == 'exit':
        return (command,)

    if command == 'help':
        return (command,)

    print(f'Неизвестная команда: {command}')
    return ('unknown', None)


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def info():
    print("\nДоступные команды:\n")
    for k, v in commands.items():
        print(f"<command> {k} - {v}")

    return None


def welcome():
    """ Выводит список комманд и возвращает ввод пользователя"""
    info()
    return None


def prompt_input():
    user_input = prompt.string("Введите команду: ")
    return user_input
