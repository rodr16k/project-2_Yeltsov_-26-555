import shlex


def _convert_value(raw: str):
    '''Приведение строки c типом к типу int/bool/str'''
    if raw.lower() in ('true', 'false'):
        return raw.lower() == 'true'

    try:
        return int(raw)
    except ValueError:
        pass

    if len(raw) > 2 and raw[0] in "\'\"" and raw[0] == raw[-1]:
        return raw[1:-1]
    raise ValueError(f'Строковое значение должно быть в кавычках: {raw!r}')


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
        tokens = shlex.split(query.strip(), posix=True)
    except ValueError as e:
        print(f'Ошибка кавычек: {e}')
    if 'where' not in tokens:
        raise ValueError('Не найдено ключевое слово \'where\'.')

    start = tokens.index('where') + 1
    where_tokens = tokens[start:]

    if not where_tokens:
        raise ValueError('Пустое условие \'where\'.')
    if len(where_tokens) % 3 != 0:
        raise ValueError('Некорректный синтаксис \'where\':'
                         'Ожидается: <column> = <value>')

    where_clause = {}

    for i in range(0, len(where_tokens), 3):
        name, eq, value = where_tokens[i], where_tokens[i+1], where_tokens[i+2]
        if eq != '=':
            raise ValueError('Некорректный синтаксис \'where\':'
                             'Ожидается: <column> = <value>')
        where_clause[name] = _convert_value(value)
    return where_clause
