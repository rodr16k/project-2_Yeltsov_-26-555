
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.parser import (
    parse_columns,
    parse_command,
    parse_insert,
    parse_select,
    parse_set_clause,
    parse_where_clause,
)
from primitive_db.utils import (
    delete_table_data,
    load_catalog,
    load_table_data,
    print_help,
    print_table,
    prompt_input,
    save_catalog,
    save_table_data,
    welcome,
)

# Управляющие функции для команд, работающих с таблицами


def _cmd_create_table(rest: str):
    catalog = load_catalog()
    table_name = rest.strip().split(maxsplit=1)[0]
    columns = parse_columns(rest)
    catalog, table_data = create_table(catalog, table_name, columns)
    save_catalog(catalog)
    save_table_data(table_name, table_data)
    print(f'Таблица {table_name} создана.')


def _cmd_list_tables(rest: str):
    catalog = load_catalog()
    list_tables(catalog)


def _cmd_drop_table(rest: str):
    table_name = rest.strip()
    if not table_name:
        raise ValueError('Укажите имя таблицы для удаления')

    catalog = load_catalog()
    catalog = drop_table(catalog, table_name)
    save_catalog(catalog)
    delete_table_data(table_name)


def _cmd_load_table(table_name):
    return load_table_data(table_name)


def _cmd_insert(rest: str):
    table_name, values = parse_insert(rest)
    table_data = _cmd_load_table(table_name)
    new_table_data = insert(table_data, values)
    save_table_data(table_name, new_table_data)
    print('Строка добавлена')


def _cmd_select(rest: str):
    table_name, where_clause = parse_select(rest)
    table_data = _cmd_load_table(table_name)
    selected = select(table_data, where_clause)
    print_table(selected)


def _cmd_delete(rest: str):
    from_table = rest.split(maxsplit=2)
    if 'from' not in from_table:
        raise ValueError(
            'Неверный синтаксис. Ожидается: delete from <имя_таблицы>')
    table_name = from_table[1]
    table_data = _cmd_load_table(table_name)
    where_clause = parse_where_clause(rest) if 'where' in rest else {}
    if not where_clause:
        raise ValueError("Для удаления строк требуется указать условие \'where\'. "
                         "Для удаления всей таблицы воспользуйтеcь \'drop_table\'")
    n = delete(table_data, where_clause)
    save_table_data(table_name, table_data)
    print(f"Удалено {n} строк из таблицы {table_name}")


def _cmd_update(rest: str):
    rest = rest.split(maxsplit=1)
    table_name, query = rest[0], rest[1]
    table_data = _cmd_load_table(table_name)
    set_clause = parse_set_clause(query)
    where_clause = parse_where_clause(query) if 'where' in query else {}
    n = update(table_data, set_clause, where_clause)
    save_table_data(table_name, table_data)
    print(f"Обновлено {n} строк в таблице {table_name}")


def _cmd_info(rest: str):
    table_name = rest.strip()
    table_data = _cmd_load_table(table_name)
    info(table_name, table_data)


def _cmd_help(rest: str):
    print_help()


HANDLERS = {
    'create_table': _cmd_create_table,
    'list_tables': _cmd_list_tables,
    'drop_table': _cmd_drop_table,
    'insert': _cmd_insert,
    'select': _cmd_select,
    'update': _cmd_update,
    'delete': _cmd_delete,
    'info': _cmd_info,
    'help': _cmd_help
}
EXIT = 'exit'


def execute_command(parsed):
    '''Вызывает соответствующую функцию из HANDLERS'''
    command, rest = parsed
    if command == EXIT:
        return EXIT
    handler = HANDLERS.get(command)
    if handler is None:
        raise ValueError(f'Неизвестная команда: {command}.')
    handler(rest)


def run():
    '''Запускает основной цикл программы'''
    welcome()

    while True:
        user_input = prompt_input()
        try:
            parsed = parse_command(user_input)
        except ValueError as e:
            print(f"Ошибка: {e}\n Попробуйте снова")
            continue
        try:
            if execute_command(parsed) == EXIT:
                break
        except (ValueError, KeyError) as e:
            print(f"Ошибка: {e}\n Попробуйте снова")
