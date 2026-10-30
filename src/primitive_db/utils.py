import json
from pathlib import Path

import prompt
from prettytable import PrettyTable

DB_DIR = Path('data')
METADATA_FILE = DB_DIR / 'metadata.json'


def print_table(table_data: dict):
    """
    Печатает таблицу в удобном формате.
    table_data: {columns: {}, rows: []}
    """
    table = PrettyTable()
    table.field_names = list(table_data['columns'].keys())
    for row in table_data['rows']:
        table.add_row(row)
    print(table)


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Управление таблицами:")
    print("<command> create_table <имя_таблицы> <столбец1:тип>\
           .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("<command> insert into <имя_таблицы> values\
           (<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select from <имя_таблицы> where \
          <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1>\
           where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> \
          where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nДополнительно:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def load_table_data(table_name: str) -> dict:
    '''Загружает данные таблицы'''

    table_path = DB_DIR / f"{table_name}.json"

    try:
        with open(table_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise KeyError(f"Таблица {table_name} не существует.")


def save_table_data(table_name, data):
    '''Сохраняет таблицу с измененными данными'''

    DB_DIR.mkdir(parents=True, exist_ok=True)
    table_path = DB_DIR / f"{table_name}.json"

    with open(table_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return True


def delete_table_data(table_name):
    """Удаляет JSON-файл таблицы, если он существует."""
    table_path = DB_DIR / f"{table_name}.json"
    table_path.unlink(missing_ok=True)


def load_catalog():
    try:
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'tables': []}


def save_catalog(catalog):
    DB_DIR.mkdir(parents=True, exist_ok=True)
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=4)


def prompt_input():
    user_input = prompt.string("Введите команду: ")
    return user_input


def welcome():
    print("===== Функции: =====\n")
    print('<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип>\
           - создать таблицу.\n',
          '<command> list_tables: - показать таблицы.\n',
          '<command> drop_table <имя_таблицы> - удалить таблицу.\n',
          '<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...)\
              - создать запись.\n',
          '<command> select from <имя_таблицы> where <столбец> = <значение> \
            - прочитать записи по условию.\n',
          '<command> update <имя_таблицы> set <столбец1> = <новое_значение1> \
            where <столбец_условия> = <значение_условия> - обновить запись.\n',
          '<command> delete from <имя_таблицы> where <столбец> = <значение> \
            - удалить запись.\n',
          '<command> info <имя_таблицы> - вывести информацию о таблице.\n',
          '<command> exit: выйти из программы.\n',
          '<command> help: справочная информация.\n'
          )
