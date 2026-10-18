#!/usr/bin/env python3
from primitive_db.engine import welcome, prompt_input, print_help
from primitive_db.utils import parse_user_input
from primitive_db.core import Table


def main():
    welcome()
    input_string = prompt_input()
    parsed_user_input = parse_user_input(input_string)
    command = parsed_user_input[0]

    match command:
        case 'unknown':
            print('Для проверки доступных комманд введите help')
        case 'create_table':
            table = Table(parsed_user_input[1], parsed_user_input[2])
            print(
                f"Таблица {parsed_user_input[1]} успешно создана со столбцами: {table.print_columns()}")
        case 'list_tables':
            pass
        case 'drop_table':
            pass
        case 'exit':
            pass
        case 'help':
            print_help()


if __name__ == "__main__":
    main()
