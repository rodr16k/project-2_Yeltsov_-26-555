import prompt
from primitive_db.utils import load_metadata, save_metadata
from primitive_db.utils import parse_user_input, prompt_input, print_help, welcome
from primitive_db.core import create_table


DB_FILE = 'db_meta.json'


def run():
    db = load_metadata(DB_FILE)
    if not db:
        db = {
            "tables": {
                "users": {
                    "columns": {"ID": "int", "name": "str", "age": "int"},
                    "rows": [
                        {"ID": 1, "name": "Peter", "age": 30}
                    ]
                }
            }
        }
    save_metadata(DB_FILE, db)

    welcome()
    input_string = prompt_input()
    parsed_user_input = parse_user_input(input_string)
    command = parsed_user_input[0]

    match command:
        case 'unknown':
            print('Для проверки доступных комманд введите help')
        case 'create_table':
            create_table(db, parse_user_input[1], parsed_user_input[2])
            print(
                f"Таблица {parsed_user_input[1]} успешно создана со столбцами: {parse_user_input[2]}")
        case 'list_tables':
            pass
        case 'drop_table':
            pass
        case 'exit':
            pass
        case 'help':
            print_help()
