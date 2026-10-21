def create_table(metadata, table_name, columns):
    """ 
    Принимает метаданные, имя таблицы и список столбцов.
    Добавляет столбец ID:int в начало.
    Возвращает обновленный словарь metadata.
    """
    if table_name in metadata['tables']:
        raise ValueError('Таблица с таким именем уже существует')

    has_id = False
    for col, type in columns.items():
        if type not in ('int', 'str', 'bool'):
            raise TypeError(f"Столбец {col} имеет недопустимый тип: {type}"
                            f"Доступные типы: int, str, bool")
        if col.lower() == 'id':
            has_id = True

    if has_id:
        all_cols = {**columns}
    else:
        all_cols = {'ID': 'int', **columns}

    metadata['tables'][table_name] = {
        'columns': all_cols,
        'rows': []
    }
    return metadata


def drop_table(metadata, table_name):
    if table_name in metadata['tables']:
        print(f'Таблица {table_name} удалена.')
        del metadata['tables'][table_name]
    else:
        raise ValueError(f"Не найдена таблица с именем {table_name}.")

    return metadata


def list_tables(metadata):
    if len(metadata['tables']) == 0:
        print('Таблицы не найдены')
        return

    for index, table in enumerate(metadata['tables'], start=1):
        print(f"{index}: {table}")
    return
