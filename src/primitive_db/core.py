from primitive_db.utils import load_metadata


def create_table(metadata, table_name, columns):
    """ 
    Принимает метаданные, имя таблицы и список столбцов.
    Добавляет столбец ID:int в начало.
    Возвращает обновленный словарь metadata.
    """
    if table_name in metadata['tables']:
        raise ValueError('Таблица с таким именем уже существует')

    for col, type in columns.items():
        if type not in ('int', 'str', 'bool'):
            raise TypeError(f"Столбец {col} имеет недопустимый тип: {type}"
                            f"Доступные типы: int, str, bool")

    all_cols = {'ID': 'int', **columns}
    metadata['tables'][table_name] = {
        'columns': all_cols,
        'rows': []
    }
    return metadata


def drop_table(metadata, table_name):
    pass
