import prompt

commands = {
    'create_tables <имя_таблицы> <столбец1:тип> <столбец2:тип>': 'создать таблицу',
    'list_tables': 'показать таблицы',
    'drop_tables <имя_таблицы>': 'удалить таблицу',
    'exit': 'выйти из программы',
    'help': 'справочная информация'
}


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
