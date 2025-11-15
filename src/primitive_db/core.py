def create_table(metadata, table_name, columns):
    """
    Она должна принимать текущие метаданные, имя таблицы и список столбцов.
    Автоматически добавлять столбец ID:int в начало списка столбцов.
    Проверять, не существует ли уже таблица с таким именем. Если да, выводить ошибку.
    Проверять корректность типов данных (только int, str, bool).
    В случае успеха, обновлять словарь metadata и возвращать его.
    """

    if table_name in metadata:
        raise ValueError('Table already exists')
    if len(columns) == 0:
        raise ValueError('Table must have at least one column')

    try:
        columns_processed = {i[0].lower(): i[1].lower() for i in [j.split(':') for j in columns]}
    except IndexError:
        raise ValueError('Invalid column format')

    for column in columns_processed:
        if columns_processed[column] not in ['int', 'str', 'bool']:
            raise ValueError('Invalid column type')
    if 'id' not in columns_processed:
        columns_processed['id'] = 'int'
    elif columns_processed['id'] != 'int':
        raise ValueError('ID must be int')
    metadata[table_name] = columns_processed
    return metadata


def drop_table(metadata, table_name):
    """
    Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
    Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    """
    if table_name not in metadata:
        raise ValueError('Table does not exist')
    del metadata[table_name]
    return metadata


def list_tables(metadata):
    if len(metadata) == 0:
        return 'Empty'
    return '\n'.join(list(metadata.keys()))
