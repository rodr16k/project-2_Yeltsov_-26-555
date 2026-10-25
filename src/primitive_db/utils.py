import json
import os
import prompt
from pathlib import Path


DB_DIR = Path('data')
METADATA_FILE = DB_DIR / 'metadata.json'


def load_table_data(table_name: str) -> dict:
    '''Загружает данные таблицы'''

    table_path = DB_DIR / f"{table_name}.json"

    try:
        with open(table_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise (f"Таблица {table_name} не существует.")


def save_table_data(table_name, data):
    '''Сохраняет таблицу с измененными данными'''

    DB_DIR.mkdir(parents=True, exist_ok=True)
    table_path = DB_DIR / f"{table_name}.json"

    with open(table_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return True


def parse_user_input(user_input: str) -> tuple:
    """ Разбирает ввод пользователя на команды и аргументы."""

    user_input_list = user_input.strip().split()

    if not user_input_list:
        raise ValueError()

    command = user_input_list[0]

    if command == 'create_table':

        if len(user_input_list) < 3:
            raise ValueError("Недостаточно аргументов для создания таблицы.")

        table_name = user_input_list[1]
        columns = {}

        for col in user_input_list[2:]:
            if ':' not in col:
                raise ValueError(
                    'Неверный формат столбцов. Ожидается: <name:type>.')

            col_name, col_type = col.split(':', 1)
            columns[col_name] = col_type

        return (command, table_name, columns)

    if command == 'list_tables':
        return (command,)

    if command == 'drop_table':

        if len(user_input_list) < 2:
            raise ValueError("Укажите имя таблицы для удаления.")
        drop_name = user_input_list[1]
        return (command, drop_name)

    if command == 'exit':
        return (command,)

    if command == 'help':
        return (command,)

    raise ValueError(
        f'Неизвестная команда: {command}.')


def prompt_input():
    user_input = prompt.string("Введите команду: ")
    return user_input


def welcome():
    print("***База данных***\n")
    print('Функции:\n'
          '<create_table> <имя_таблицы> <столбец1:тип> <столбец2:тип>'
          ' - создать таблицу,\n'
          '<list_tables>: - показать таблицы,\n'
          '<drop_table> <имя_таблицы> - удалить таблицу,\n'
          '<exit>: выйти из программы,\n'
          '<help>: справочная информация.\n'
          )
