import pymysql
import Config
from ConnDB import connection

try:
    result_query = None
    with connection.cursor() as cursor:
        while True:
            print('Здравствуйте авторизуйтесь под своей учётной записью.')
            login = input('Введите логин: ')
            password = input('Введите пароль: ')
            Autorisation_query = f""" SELECT id FROM user WHERE '{login}' = login AND '{password}' = password """
            cursor.execute(Autorisation_query)
            id_query = cursor.fetchall()
            if id_query:
                print(f'Авторизация успешна, ваш айди: {id_query}')
                while True:
                    print("Выберите действие: "
                          "\n 1 - отобразить 2 активных на данный момент перевода"
                          "\n 2 - подтвердить перевод"
                          "\n 3 - рассчитать сумму налогов перевода"
                          "\n 4 - выход")
                    es = input('Ввод: ')
                    if es == 1:
                        active_transfers_query = f""" SELECT * FROM history WHERE received_user_id = {id_query} AND status = 'active' LIMIT 2 """
                        cursor.execute(active_transfers_query)
                        result_query = cursor.fetchall()
                        if result_query:
                            print(result_query)
                        else:
                            print('На данный момент у вас нету активных переводов')
                    if es == 2:
                        print('Введите айди АКТИВНОГО перевода')
                        trans_id = input()
                        commit_transfers_query = f""" UPDATE history WHERE received_user_id = {id_query} AND id = {trans_id} SET status = 'delivered';
                                                       SELECT * FROM history WHERE received_user_id = {id_query} AND id = {trans_id}"""
                        cursor.execute(commit_transfers_query)
                        result_query = cursor.fetchall()
                        connection.commit()
                        if result_query:
                            print(result_query)
                        else:
                            print('Использован неверный айди или это не ваш перевод или такого перевода на существует.')
            else:
                print('Неверный логин или пароль'
                        '\nНажмите 1 что бы вернуться в начало'
                        '\nНажмите 2 что бы выйти')
                sp = int(input())
                if sp == 2:
                    print('До свидания!')
                    break
except Exception as ex:
    print('Программа завершена с ошибками')
    print(ex)
finally:
    print('Программа завершена')
    connection.close