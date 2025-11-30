import os

from ..decorators import confirm_action, log_time
from .utils import META_FILE, load_table_data, save_metadata, save_table_data
from typing import Optional


def create_table(metadata: dict, table_name: str, columns: list) -> dict:
    """
    Creates a new table with the given columns.
    :param metadata (dict): current metadata
    :param table_name (str): name of the table to create
    :param columns (list): list of columns to create, in the format "name:type"

    :return dict: updated metadata
    """

    if table_name in metadata:
        raise ValueError("Table already exists")
    if len(columns) == 0:
        raise ValueError("Table must have at least one column")

    try:
        columns_processed = {
            i[0].lower(): i[1].lower() for i in [j.split(":") for j in columns]
        }
    except IndexError:
        raise ValueError("Invalid column format")

    for column in columns_processed:
        if columns_processed[column] not in ["int", "str", "bool"]:
            raise ValueError("Invalid column type")
    if "id" not in columns_processed:
        columns_processed["id"] = "int"
    elif columns_processed["id"] != "int":
        raise ValueError("ID must be int")
    columns_ordered = {}
    order = 1
    for column in columns_processed:
        if column == "id":
            columns_ordered[0] = {"name": column, "type": columns_processed[column]}
        else:
            columns_ordered[order] = {"name": column, "type": columns_processed[column]}
            order += 1
    metadata[table_name] = columns_ordered
    save_table_data(table_name, {})
    return metadata


@confirm_action
def drop_table(table_name: str, metadata: dict) -> None:
    """
    Deletes table data and metadata.
    :param table_name (str): name of the table to delete
    :param metadata (dict): current metadata
    """
    os.remove(f"data/{table_name}.json")
    metadata.pop(table_name)
    save_metadata(META_FILE, metadata)


def list_tables(metadata: dict) -> str:
    """
    Lists all tables.
    :param metadata (dict): current metadata
    :return str: list of tables
    """
    if len(metadata) == 0:
        return "Empty"
    return "\n".join(list(metadata.keys()))


@log_time
def insert(metadata: dict, table_name: str, values: list) -> dict:
    """
    Inserts a new record into a table.

    :param metadata (dict): current metadata
    :param table_name (str): name of the table to insert into
    :param values (list): values to insert
    :return dict: new data with inserted record
    """
    if len(values) != len(metadata[table_name]) - 1:
        raise ValueError("Invalid number of values")
    for i in range(len(values)):
        if metadata[table_name][str(i + 1)]["type"] == "int":
            try:
                values[i] = int(values[i])
            except ValueError:
                raise ValueError("Invalid int value")
        elif metadata[table_name][str(i + 1)]["type"] == "str":
            try:
                values[i] = str(values[i])
            except ValueError:
                raise ValueError("Invalid int value")
        elif metadata[table_name][str(i + 1)]["type"] == "bool":
            if values[i].lower() not in ["true", "false"]:
                raise ValueError("Invalid bool value")
            values[i] = values[i].lower()
    data = load_table_data(table_name)

    new_id = max([int(i) for i in data.keys()], default=0) + 1
    data[new_id] = {
        metadata[table_name][str(i + 1)]["name"]: str(values[i])
        for i in range(len(values))
    }
    return data


@log_time
def select(table_data: dict, where_clause: Optional[dict] = None) -> dict:
    """
    Selects records from a table based on a where clause.
    :param table_data (dict): current data of the table
    :param where_clause (dict): optional where clause to filter records

    :return dict: filtered records if where_clause is not None, otherwise all records
    """
    if where_clause is None:
        return table_data
    if list(where_clause.keys())[0] == "id":
        return {where_clause["id"]: table_data[where_clause["id"]]}
    return {
        k: v
        for k, v in table_data.items()
        if all(v[i] == where_clause[i] for i in where_clause)
    }


def update(table_data: dict, set_clause: list, where_clause: dict) -> dict:
    """
    Selects records from a table based on a where clause and updates them with set_clause.

    :param table_data (dict): current data of the table
    :param set_clause (list): dictionary with key as the column name and value as the new value
    :param where_clause (dict): dictionary with key as the column name and value as the value to match

    :return dict: updated records
    """
    for_update = select(table_data, where_clause)
    for k in for_update:
        table_data[k][set_clause[0]] = set_clause[1]

    return table_data


@confirm_action
def delete(table_name: str, table_data: dict, where_clause: dict) -> None:
    """
    Deletes records from a table based on a where clause.
    :param table_name (str): name of the table
    :param table_data (dict): current data of the table
    :param where_clause (dict): dictionary with key as the column name and value as the value to match

    :return dict: updated records
    """
    for_delete = select(table_data, where_clause)

    for k in for_delete:
        del table_data[k]
    save_table_data(table_name, table_data)
