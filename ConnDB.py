import pymysql
from Config import host, login, password, database

try:
    connection = pymysql.connect(
        host=host,
        user=login,
        password=password,
        database=database,
        cursorclass = pymysql.cursors.DictCursor
    )
    print('Соединение успешно')

except Exception as ex:
    print('Программа завершена с ошибками')
    print(ex)
