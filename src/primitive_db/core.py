from .utils import load_table_data, save_table_data


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
    columns_ordered = {}
    order = 1
    for column in columns_processed:
        if column == 'id':
            columns_ordered[0] = {
                'name': column,
                'type': columns_processed[column]
            }
        else:
            columns_ordered[order] = {
                'name': column,
                'type': columns_processed[column]
            }
            order += 1
    metadata[table_name] = columns_ordered
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


def insert(metadata, table_name, values):
    """
    Проверяет, существует ли таблица.
    Проверяет, что количество переданных значений соответствует количеству столбцов (минус ID).
    Валидирует типы данных для каждого значения в соответствии со схемой в metadata.
    Генерирует новый ID (например, max(IDs) + 1 или len(data) + 1).
    Добавляет новую запись (в виде словаря) в данные таблицы и возвращает их.
    """
    if table_name not in metadata:
        raise ValueError('Table does not exist')
    if len(values) != len(metadata[table_name]) - 1:
        raise ValueError('Invalid number of values')
    for i in range(len(values)):
        if metadata[table_name][str(i + 1)]['type'] == 'int':
            try:
                values[i] = int(values[i])
            except ValueError:
                raise ValueError('Invalid int value')
        elif metadata[table_name][str(i + 1)]['type'] == 'str':
            try:
                values[i] = str(values[i])
            except ValueError:
                raise ValueError('Invalid int value')
        elif metadata[table_name][str(i + 1)]['type'] == 'bool':
            if values[i].lower() not in ['true', 'false']:
                raise ValueError('Invalid bool value')
            values[i] = values[i].lower()
    data = load_table_data(table_name)

    new_id = max([int(i) for i in data.keys()], default=0) + 1
    data[new_id] = {metadata[table_name][str(i + 1)]['name']: str(values[i]) for i in range(len(values))}
    save_table_data(table_name, data)
    return data


def select(table_data, where_clause=None):
    """
    Если where_clause не задан, возвращает все данные.
    Если задан (например, {'age': 28}), фильтрует и возвращает только подходящие записи.
    """
    if where_clause is None:
        return table_data
    print(where_clause)
    return {k: v for k, v in table_data.items() if all(v[i] == where_clause[i] for i in where_clause)}


def update(table_data, set_clause, where_clause):
    """
    Находит записи по where_clause.
    Обновляет в найденных записях поля согласно set_clause.
    Возвращает измененные данные.
    """
    for_update = select(table_data, where_clause)
    for k in for_update:
        table_data[k][set_clause[0]] = set_clause[1]
    """
    for k, v in table_data.items():
        if all(v[i] == where_clause[i] for i in where_clause):
            v[set_clause[0]] = set_clause[1]
            table_data[k] = v"""
    return table_data


def delete(table_data, where_clause):
    """
    Находит записи по where_clause и удаляет их.
    Возвращает измененные данные.
    """
    for_delete = select(table_data, where_clause)

    for k in for_delete:
        del table_data[k]
    return table_data
