import prompt


def welcome():
    print("Первая попытка запустить проект!\n")
    print('***')

    commands = {
        'exit': 'выйти из программы',
        'help': 'справочная информация'
    }

    for k, v in commands.items():
        print(f"<command> {k} - {v}")

    prompt.string("Введите команду: ")
