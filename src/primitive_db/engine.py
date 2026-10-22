from primitive_db.core import create_table, drop_table, list_tables, print_help
from primitive_db.utils import (
    load_metadata,
    parse_user_input,
    prompt_input,
    save_metadata,
    welcome,
)

DB_FILE = 'db_meta.json'


def run():
    welcome()
    try:
        db = load_metadata(DB_FILE)
    except FileNotFoundError as e:
        print(e)

    if not db:
        db = {'tables': {}}

    while True:
        input_str = prompt_input()

        try:
            parsed_user_input = parse_user_input(input_str)
        except ValueError as e:
            print(e, "Попробуйте снова.")
            continue

        command = parsed_user_input[0]
        if command == 'exit':
            break

        match command:
            case 'create_table':
                try:
                    db = create_table(
                        db, parsed_user_input[1], parsed_user_input[2])
                    print(
                        f"Таблица {parsed_user_input[1]}"
                        f" успешно создана со столбцами: {parsed_user_input[2]}")
                except ValueError as e:
                    print(e, 'Попробуйте снова.')
                except TypeError as e:
                    print(e, 'Попробуйте снова.')
            case 'list_tables':
                try:
                    list_tables(db)
                except ValueError as e:
                    print(e)
            case 'drop_table':
                try:
                    db = drop_table(db, parsed_user_input[1])
                except ValueError as e:
                    print(e)
            case 'help':
                print_help()

        save_metadata(DB_FILE, db)
