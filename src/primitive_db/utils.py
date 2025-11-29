import json

import prettytable

META_FILE = "metadata.json"


def load_metadata(filepath: str) -> dict:
    """
    Loads metadata from a file.
    :param filepath (str): path to the file
    :return dict: metadata
    """
    try:
        with open(filepath) as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


def save_metadata(filepath: str, data: dict) -> None:
    """
    Saves metadata to a file.
    :param filepath (str): path to the file
    :param data (dict): metadata
    """
    with open(filepath, 'w') as f:
        f.write(json.dumps(data, indent=2, sort_keys=False))


def load_table_data(table_name: str) -> dict:
    """
    Loads table data from a file.
    :param table_name (str): name of the table
    :return dict: table data
    """
    with open(f'data/{table_name}.json') as f:
        return json.loads(f.read())


def save_table_data(table_name: str, data: dict) -> None:
    """
    Saves table data to a file.
    :param table_name (str): name of the table
    :param data (dict): table data
    """
    with open(f'data/{table_name}.json', 'w') as f:
        f.write(json.dumps(data, indent=2))


def pretty_print(data: dict, table_metadata: dict) -> None:
    """
    Prints table data in a pretty format.
    :param data (dict): table data
    :param table_metadata (dict): metadata of the table
    """
    table = prettytable.PrettyTable()
    names = []
    for column in range(len(table_metadata)):
        names.append(table_metadata[str(column)]['name'])
    table.field_names = names
    names.remove('id')
    for row in data:
        table.add_row([row, *[data[row][name] for name in names]])
    print(table)
