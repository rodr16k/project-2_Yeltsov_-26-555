def create_table(metadata, table_name, columns):
    """
    Принимает каталог (metadata), имя таблицы и словарь столбцов {имя: тип}.
    Добавляет столбец ID:int в начало, если его нет.
    Возвращает кортеж:
        (обновлённый каталог, начальные данные таблицы {'columns': {...}, 'rows': []}).
    """
    if table_name in metadata['tables']:
        raise ValueError('Таблица с таким именем уже существует')

    has_id = False
    for col, col_type in columns.items():
        if col_type not in ('int', 'str', 'bool'):
            raise TypeError(
                f"Столбец {col} имеет недопустимый тип: {col_type}\n"
                f"Доступные типы: int, str, bool"
            )
        if col.lower() == 'id':
            has_id = True

    if has_id:
        all_cols = {**columns}
    else:
        all_cols = {'ID': 'int', **columns}

    metadata['tables'].append(table_name)

    table_data = {
        'columns': all_cols,
        'rows': []
    }

    return metadata, table_data


def drop_table(metadata, table_name):
    if table_name in metadata['tables']:
        metadata['tables'].remove(table_name)
        print(f'Таблица {table_name} удалена.')
    else:
        raise ValueError(f"Не найдена таблица с именем {table_name}.")

    return metadata


def list_tables(metadata):
    if 'tables' not in metadata or len(metadata['tables']) == 0:
        raise ValueError('Таблицы не найдены')

    print("Сохраненные таблицы:")

    for index, table in enumerate(metadata['tables'], start=1):
        print(f"{index}: {table}")


# CRUD Функции

TYPE_MAP = {'int': int, 'str': str, 'bool': bool}


def insert(table_data: dict, values: list):
    """
    Добавляет строку в таблицу. 
    ID генерируется автоматически.
    """
    columns = table_data['columns']
    data_columns = list(columns.items())[1:]

    if len(values) != len(data_columns):
        raise ValueError(
            f'Ожидается {len(data_columns)} значений, получено {len(values)}.')

    for val, (col_name, type_name) in zip(values, data_columns):
        if type(val) is not TYPE_MAP[type_name]:
            raise ValueError(
                f'Столбец "{col_name}": значение {val!r} имеет тип '
                f'{type(val).__name__}, ожидается {type_name}.')

    new_id = max((row[0] for row in table_data['rows']), default=-1) + 1
    table_data['rows'].append([new_id, *values])
    return table_data


def _col_index(columns):
    """Имя колонки -> позиция в строке."""
    return {name: i for i, name in enumerate(columns)}


# where_clause после парсинга имеет вид {'столбец': значение}
def select(table_data, where_clause=None) -> dict:
    if where_clause == None:
        return table_data

    col_index = _col_index(table_data['columns'])

    for col in where_clause:
        if col not in col_index:
            raise ValueError(f'В таблице нет столбца {col}')

    matches = []
    for row in table_data['rows']:
        if all(row[col_index[col]] == val for col, val in where_clause.items()):
            matches.append(row)

    return {
        'columns': table_data['columns'],
        'rows': matches
    }


def _matches(row, where_clause, col_index):
    return all(row[col_index[c]] == v for c, v in where_clause.items())


def update(table_data, set_clause, where_clause):
    """Обновляет строки по условию. Возвращает число обновлённых строк."""
    col_index = _col_index(table_data['columns'])

    for col in set_clause:
        if col not in col_index:
            raise ValueError(f'В таблице нет столбца "{col}".')

    updated = 0
    for row in table_data['rows']:
        if not _matches(row, where_clause, col_index):
            continue
        for col, val in set_clause.items():
            row[col_index[col]] = val
        updated += 1

    return updated


def delete(table_data, where_clause):
    """Удаляет из таблицы строки по условию"""

    col_index = _col_index(table_data['columns'])

    for col in where_clause:
        if col not in col_index:
            raise ValueError(f'В таблице нет столбца "{col}".')

    before = len(table_data['rows'])

    table_data['rows'] = [row for row in table_data['rows']
                          if not _matches(row, where_clause, col_index)]

    n_deleted = before - len(table_data['rows'])

    return n_deleted


def info(table_name: str, table_data: dict):
    print(f'===== Информация о таблице {table_name}: =====\n')
    print(f'Столбцы:\n {table_data['columns']}')
    print(f'Всего строк:\n {len(table_data['rows'])}')
