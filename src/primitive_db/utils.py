import json

import prettytable


def load_metadata(filepath):
    try:
        with open(filepath) as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, 'w') as f:
        f.write(json.dumps(data, indent=2, sort_keys=False))


def load_table_data(table_name):
    try:
        with open(f'data/{table_name}.json') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


def save_table_data(table_name, data):
    with open(f'data/{table_name}.json', 'w') as f:
        f.write(json.dumps(data, indent=2))


def pretty_print(data, table_metadata):
    table = prettytable.PrettyTable()
    names = []
    for column in range(len(table_metadata)):
        names.append(table_metadata[str(column)]['name'])
    table.field_names = names
    print(data)
    names.remove('id')
    for row in data:
        table.add_row([row, *[data[row][name] for name in names]])
    print(table)
