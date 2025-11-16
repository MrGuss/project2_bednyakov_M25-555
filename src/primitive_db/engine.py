import shlex

import prompt

from .core import create_table, delete, drop_table, insert, list_tables, select, update
from .utils import load_metadata, load_table_data, pretty_print, save_metadata, save_table_data


def run():
    while True:
        """
        Загружайте актуальные метаданные с помощью load_metadata.
        Запрашивайте ввод у пользователя.
        Разбирайте введенную строку на команду и аргументы.
        Подсказка: Для надежного разбора строки используйте библиотеку shlex. args = shlex.split(user_input).
        Используйте if/elif/else или match/case для вызова соответствующей функции из core.py.
        После каждой успешной операции (create_table, drop_table) сохраняйте измененные метаданные
        с помощью save_metadata.
        """
        metadata = load_metadata('metadata.json')
        cmd = prompt.string('>>>Введите команду: ')
        args = shlex.split(cmd)

        try:
            if args[0] == 'exit':
                break
            elif args[0] == 'help':
                print_help()
            elif args[0] == 'create_table':
                metadata = create_table(metadata, args[1], args[2:])
                print(f"Table {args[1]} created")
                save_metadata('metadata.json', metadata)
            elif args[0] == 'list_tables':
                print(list_tables(metadata))
            elif args[0] == 'drop_table':
                metadata = drop_table(metadata, args[1])
                print(f"Table {args[1]} deleted")
                save_metadata('metadata.json', metadata)
            elif args[0] == 'insert' and args[1] == 'into':
                data = insert(metadata, args[2], args[3:])
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
                        raise ValueError("Invalid SELECT command")
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
                        raise ValueError("Invalid UPDATE command")

                    if len(set_tokens) == 3 and set_tokens[1] == "=":
                        set_clause = [set_tokens[0].lower(), set_tokens[2]]
                    elif len(set_tokens) == 1:
                        set_clause = set_tokens[0].split('=')
                    else:
                        raise ValueError("Invalid UPDATE command")
                else:
                    raise ValueError("Invalid UPDATE command")
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
                        raise ValueError("Invalid DELETE command")
                else:
                    raise ValueError("Invalid DELETE command")

                updated_data = delete(data, where_clause)
                save_table_data(args[2], updated_data)
            else:
                print(f"Функции {args[0]} нет. Попробуйте снова.")
        except ValueError as e:
            print("Некорректные аргументы. Попробуйте снова. Ошибка:")
            print(e)


def print_help():
    """Prints the help message for the current mode."""

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
