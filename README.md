# dummydb

dummydb - простой база данных для учебных целей

## Установка

Требования:
- Python 3.8+
- Poetry

```bash
make install
```

## Запуск

```bash
make project
```

## Управление таблицами

```
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> insert into <имя_таблицы> <столбец1> <значение1> .. - добавить запись в таблицу
<command> select from <имя_таблицы> - выбрать все записи из таблицы
<command> select from <имя_таблицы> where <столбец> = <значение> - выбрать записи из таблицы
<command> update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение> - обновить запись
<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись

Общие команды:
<command> exit - выход из программы
<command> help - справочная информация
```

## Демо

[![asciicast](https://asciinema.org/a/759108.svg)](https://asciinema.org/a/759108)