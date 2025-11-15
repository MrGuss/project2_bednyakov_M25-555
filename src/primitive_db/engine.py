import shlex

import prompt

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


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
        data = load_metadata('metadata.json')
        cmd = prompt.string('>>>Введите команду: ')
        args = shlex.split(cmd)
        try:
            if args[0] == 'exit':
                break
            elif args[0] == 'help':
                print_help()
            elif args[0] == 'create_table':
                data = create_table(data, args[1], args[2:])
                print(f"Table {args[1]} created")
                save_metadata('metadata.json', data)
            elif args[0] == 'list_tables':
                print(list_tables(data))
            elif args[0] == 'drop_table':
                data = drop_table(data, args[1])
                print(f"Table {args[1]} deleted")
                save_metadata('metadata.json', data)
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

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")
