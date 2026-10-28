import shlex


# Ввод принимается в виде строки: ...set <col_1> = <val1> where ...
def parse_set_clause(query: str) -> dict:
    '''
    Выполняет разбор ввода условия set.
    Возвращает словарь {col:value}
    '''
    try:
        # получаем токены ['set', 'col', '=', 'val']
        tokens = shlex.split(query.strip(), posix=False)
    except ValueError as e:
        print(f'Ошибка кавычек: {e}')

    if 'set' not in tokens:
        raise ValueError('Не найдено ключевое слово \'set\'.')

    start = tokens.index('set') + 1
    set_tokens = []
    for token in tokens[start:]:
        if token == 'where':
            break
        set_tokens.append(token)

    if not set_tokens:
        raise ValueError('Пустое условие \'set\'.')
    if len(set_tokens) % 3 != 0:
        raise ValueError('Некорректный синтаксис \'set\':'
                         'Ожидается: <column> = <value>')

    set_clause = {}
    for i in range(0, len(set_tokens), 3):
        name, eq, value = set_tokens[i], set_tokens[i+1], set_tokens[i+2]
        if eq != '=':
            raise ValueError('Некорректный синтаксис \'set\':'
                             'Ожидается: <column> = <value>')
        set_clause[name] = _convert_value(value)
    return set_clause


def parse_where_clause(query: str) -> dict:
    '''
    Выполняет разбор ввода условия where.
    Возвращает словарь {col:value}
    '''
    try:
        # получаем токены ['where', 'col', '=', 'val']
        tokens = shlex.split(query.strip(), posix=False)
    except NameError as e:
        raise (f'Ошибка кавычек: {e}')
    if 'where' not in tokens:
        raise ValueError('Не найдено ключевое слово \'where\'.')

    start = tokens.index('where') + 1
    where_tokens = tokens[start:]

    if not where_tokens:
        raise NameError('Пустое условие \'where\'.')
    if len(where_tokens) % 3 != 0:
        raise NameError('Некорректный синтаксис \'where\':'
                        'Ожидается: <column> = <value>')

    where_clause = {}

    for i in range(0, len(where_tokens), 3):
        name, eq, value = where_tokens[i], where_tokens[i+1], where_tokens[i+2]
        if eq != '=':
            raise NameError('Некорректный синтаксис \'where\':'
                            'Ожидается: <column> = <value>')
        where_clause[name] = _convert_value(value)
    return where_clause


def parse_columns(columns_str: str) -> dict:
    """'name:str age:int' -> {'name': 'str', 'age': 'int'}"""
    columns = {}
    for col in columns_str.split():
        if ':' in col:
            name, col_type = col.split(':', 1)
            columns[name] = col_type
        else:
            continue
    if not columns:
        raise NameError(
            f'Неверный формат столбца "{col}". Ожидается: <name:type>.')
    return columns


def parse_command(query: str) -> tuple:
    """
    Достает из ввода первую команду.
    Возвращает команду и остальную строку.
    """
    parts = query.strip().split(maxsplit=1)
    if not parts:
        raise ValueError('Пустой ввод.')

    command = parts[0]
    rest = parts[1] if len(parts) > 1 else ''
    return (command, rest)


# select from <имя_таблицы> where <столбец> = <значение>
def parse_select(rest: str) -> tuple[str, dict]:
    parts = rest.strip().split(maxsplit=1)
    if len(parts) != 2 or parts[0] != 'from':
        raise ValueError(
            'Неверный синтаксис. Ожидается: '
            'select from <имя_таблицы> [where <столбец> = <значение>]'
        )

    remainder = parts[1].strip()

    if ' where ' in remainder:
        table_name, where_str = remainder.split(' where ', 1)
        where_clause = parse_where_clause('where ' + where_str.strip())
    else:
        table_name, where_clause = remainder, {}

    table_name = table_name.strip()
    if not table_name:
        raise ValueError('Не указано имя таблицы')

    return table_name, where_clause


# insert into <имя_таблицы> values (<значение1>, <значение2>, ...)

def parse_insert(rest: str) -> tuple[str, list]:
    """
    'into users values (Alice, 30)' -> ('users', ['Alice', 30])
    """
    parts = rest.strip().split(maxsplit=3)
    if len(parts) != 4:
        raise ValueError(
            "Неверный синтаксис. Ожидается: "
            "insert into <имя_таблицы> values (<значение1>, <значение2>, ...)"
        )
    kw_into, table_name, kw_values, values_str = parts

    if kw_into != 'into':
        raise ValueError(f"Ожидалось 'into', получено '{kw_into}'")
    if kw_values != 'values':
        raise ValueError(f"Ожидалось 'values', получено '{kw_values}'")
    if not table_name:
        raise ValueError('Не указано имя таблицы')

    values = _parse_values(values_str)
    return table_name, values


def _parse_values(values_str: str) -> list:
    """'(Alice, 30, true)' -> ['Alice', 30, True]"""
    s = values_str.strip()
    if not (s.startswith('(') and s.endswith(')')):
        raise ValueError(
            "Список значений должен быть в скобках: (v1, v2, ...)"
        )

    inner = s[1:-1]
    if not inner.strip():
        raise ValueError('Список значений пуст')

    raw_tokens = _split_top_level(inner)
    return [_convert_value(t) for t in raw_tokens]


def _split_top_level(inner: str) -> list[str]:
    """Режет по запятым вне кавычек. Сохраняет кавычки в токенах."""
    tokens, buf = [], []
    quote = None
    for ch in inner:
        if quote is not None:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
            buf.append(ch)
        elif ch == ',':
            tokens.append(''.join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if quote is not None:
        raise ValueError('Незакрытая кавычка в списке значений')
    tokens.append(''.join(buf).strip())

    if any(t == '' for t in tokens):
        raise ValueError('Пустое значение в списке')
    return tokens


def _convert_value(raw: str):
    '''Приведение строки c типом к типу int/bool/str'''
    if raw.lower() in ('true', 'false'):
        return raw.lower() == 'true'

    try:
        return int(raw)
    except ValueError:
        pass

    if len(raw) >= 2 and raw[0] in ['"', "'"] and raw[0] == raw[-1]:
        return raw[1:-1]
    raise ValueError(f'Строковое значение должно быть в кавычках: {raw!r}')
