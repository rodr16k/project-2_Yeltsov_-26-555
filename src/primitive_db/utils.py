def parse_user_input(user_input: str) -> (str):
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
