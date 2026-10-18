class Table:
    def __init__(self, name: str, columns: dict):
        self.name = name
        self.columns = columns

    def print_columns(self):
        cols_list = []
        for col, type in self.columns.items():
            col_info = col + ":" + type
            cols_list.append(col_info)

        cols_str = ', '.join(cols_list)
        return cols_str

    def create_table(self, name, columns):
        pass

    def list_tables(self):
        pass

    def drop_table(self, name):
        pass


# ***База данных***

# Функции:
# <command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
# <command> list_tables - показать список всех таблиц
# <command> drop_table <имя_таблицы> - удалить таблицу
# <command> exit - выход из программы
# <command> help - справочная информация

# >>>Введите команду: _
