from primitive_db.core import create_table, drop_table, list_tables, print_help, insert, select, delete, update
from primitive_db.utils import (
    load_table_data,
    parse_user_input,
    prompt_input,
    save_table_data,
    welcome,
)
from primitive_db.parser import _convert_value, parse_set_clause, parse_where_clause
import prettytable


# Управляющие функции для команд, работающих с таблицами

def _cmd_load_table(table_name):
    try:
        load_table_data(table_name)
    except FileNotFoundError as e:
        raise ValueError(f"Таблица {table_name} не найдена.")


def _cmd_insert(table_name, *raw_values):
    values = tuple(_convert_value(v) for v in raw_values)
    table_data = load_table_data(table_name)
    table_data = insert(table_data, values)
    save_table_data(table_name, table_data)
    print('Строка добавлена')


def _cmd_select(table_name, where_str):
    where_clause = parse_where_clause(where_str) if where_str else None
    table_data = _cmd_load_table(table_name)
    selected = select(table_data, where_clause)
    print(selected)


def _cmd_delete(table_name, where_str):
    table_data = _cmd_load_table(table_name)
    where_clause = parse_where_clause(where_str) if where_str else {}
    if not where_clause:
        raise ValueError('Для удаления строк требуется указать условие \'where\'. \
                         Для удаления всей таблицы воспользуйтель \'drop_table\'')
    n = delete(table_data, where_clause)
    save_table_data(table_name, table_data)
    print(f"Удалено {n} строк из таблицы {table_name}")


def _cmd_update(table_name, set_str, where_str):
    table_data = _cmd_load_table(table_name)
    set_clause = parse_set_clause(set_str)
    where_clause = parse_where_clause(where_str) if where_str else {}
    n = update(table_data, set_clause, where_clause)
    save_table_data(table_name, table_data)
    print(f"Обновлено {n} строк в таблице {table_name}")


HANDLERS = {
    'create_table': _cmd_create_table,
    'list_tables': _cmd_list_tables,
    'drop_table': _cmd_drop_table,
    'insert': _cmd_insert,
    'select': _cmd_select,
    'update': _cmd_update,
    'delete': _cmd_delete
}
EXIT = 'exit'


def execute_command(parsed):
    command, *args = parsed
    if command == EXIT:
        return EXIT
    handler = HANDLERS.get(command)
    if handler is None:
        raise ValueError(f'Неизвестная команда: {command}.')
    handler(*args)


def run():
    welcome()

    while True:
        user_input = prompt_input()
        try:
            parsed = parse_user_input(user_input)
            if execute_command(parsed) == EXIT:
                break
        except (ValueError, TypeError) as e:
            print(f"Ошибка: {e}. Попробуйте снова")
