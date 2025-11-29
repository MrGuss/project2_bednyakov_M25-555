import shlex

import prompt

from ..decorators import handle_db_errors
from .core import create_table, delete, drop_table, insert, list_tables, select, update
from .utils import META_FILE, load_metadata, load_table_data, pretty_print, save_metadata, save_table_data


def run() -> None:
    while True:
        """
        Run the database engine.
        """
        metadata = load_metadata(META_FILE)
        cmd = prompt.string('>>>Введите команду: ')
        args = shlex.split(cmd)
        if parse_command(args, metadata) == 1:
            break


def print_help() -> None:
    """
    Prints the help message.
    """

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert into <имя_таблицы> <столбец1> <значение1> .. - добавить запись в таблицу")
    print("<command> select from <имя_таблицы> - выбрать все записи из таблицы")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - выбрать записи из таблицы")
    print("<command> update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение> - обновить запись")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


@handle_db_errors
def parse_command(args: list, metadata: dict) -> int:
    """
    Parses the command.

    :param args (list): list of arguments
    :param metadata (dict): current metadata

    :return int: exit code
    """
    if args[0] == 'exit':
        return 1
    elif args[0] == 'help':
        print_help()
    elif args[0] == 'create_table':
        metadata = create_table(metadata, args[1], args[2:])
        save_metadata(META_FILE, metadata)
    elif args[0] == 'list_tables':
        print(list_tables(metadata))
    elif args[0] == 'drop_table':
        drop_table(args[1], metadata)
    elif args[0] == 'insert' and args[1] == 'into':
        data = insert(metadata, args[2], args[3:])
        save_table_data(args[2], data)
    elif args[0] == 'select' and args[1] == 'from':
        data = load_table_data(args[2])
        if "where" in args:
            w_index = args.index("where")
            where_tokens = args[w_index+1:]
            if len(where_tokens) == 3 and where_tokens[1] == "=":
                where_clause = {where_tokens[0].lower(): where_tokens[2]}
            elif len(where_tokens) == 1:
                where_clause = where_tokens[0].split('=')
                where_clause = {where_clause[0].lower(): where_clause[1]}
            else:
                print("Invalid SELECT command")
                return 0
            selected = select(data, where_clause)
        else:
            selected = select(data, None)
        pretty_print(selected, metadata[args[2]])
    elif args[0] == 'update':
        data = load_table_data(args[1])
        if "where" in args and "set" in args:
            w_index = args.index("where")
            s_index = args.index("set")

            set_tokens = args[s_index+1:w_index]
            where_tokens = args[w_index+1:]

            if len(where_tokens) == 3 and where_tokens[1] == "=":
                where_clause = {where_tokens[0].lower(): where_tokens[2]}
            elif len(where_tokens) == 1:
                where_clause = where_tokens[0].split('=')
                where_clause = {where_clause[0].lower(): where_clause[1]}
            else:
                print("Invalid UPDATE command")
                return 0

            if len(set_tokens) == 3 and set_tokens[1] == "=":
                set_clause = [set_tokens[0].lower(), set_tokens[2]]
            elif len(set_tokens) == 1:
                set_clause = set_tokens[0].split('=')
            else:
                print("Invalid UPDATE command")
                return 0
        else:
            print("Invalid UPDATE command")
            return 0
        updated_data = update(data, set_clause, where_clause)
        save_table_data(args[1], updated_data)
    elif args[0] == 'delete':
        data = load_table_data(args[2])
        if "where" in args:
            w_index = args.index("where")
            where_tokens = args[w_index+1:]
            if len(where_tokens) == 3 and where_tokens[1] == "=":
                where_clause = {where_tokens[0].lower(): where_tokens[2]}
            elif len(where_tokens) == 1:
                where_clause = where_tokens[0].split('=')
                where_clause = {where_clause[0].lower(): where_clause[1]}
            else:
                print("Invalid DELETE command")
                return 0
        else:
            print("Invalid DELETE command")
            return 0
        delete(args[2], data, where_clause)
    else:
        print(f"Функции {args[0]} нет. Попробуйте снова.")
    return 0
