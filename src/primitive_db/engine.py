from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import (
    load_metadata,
    parse_user_input,
    prompt_input,
    save_metadata,
)

DB_FILE = 'db_meta.json'

# src/primitive_db/engine.py


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


def run():
    db = load_metadata(DB_FILE)

    while True:
        input_str = prompt_input()
        parsed_user_input = parse_user_input(input_str)
        command = parsed_user_input[0]
        if command == 'exit':
            break

        match command:
            case 'unknown':
                print('Для проверки доступных комманд введите help')
            case 'create_table':
                db = create_table(
                    db, parsed_user_input[1], parsed_user_input[2])
                print(
                    f"Таблица {parsed_user_input[1]}"
                    f" успешно создана со столбцами: {parsed_user_input[2]}")
            case 'list_tables':
                print("Сохраненные таблицы: ")
                list_tables(db)
            case 'drop_table':
                db = drop_table(db, parsed_user_input[1])
            case 'help':
                print_help()

        save_metadata(DB_FILE, db)
