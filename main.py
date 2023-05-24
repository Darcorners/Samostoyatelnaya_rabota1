import re
import pymysql
import Config
from ConnDB import connection

try:
    result_query = None
    with connection.cursor() as cursor:
        while True:
            print('Здравствуйте авторизуйтесь под своей учётной записью.\n')
            login = input('Введите логин: ')
            password = input('Введите пароль: ')
            Autorisation_query = f""" SELECT id FROM user WHERE '{login}' = login AND '{password}' = password """
            cursor.execute(Autorisation_query)
            id_query = cursor.fetchone()
            if id_query != None:
                id_query = id_query["id"]
                print(f'\nАвторизация успешна, ваш айди: {id_query}')
                while True:
                    result_query = None
                    print("\nВыберите действие: "
                          "\n 1 - отобразить 2 активных на данный момент перевода"
                          "\n 2 - подтвердить перевод"
                          "\n 3 - рассчитать сумму налогов перевода"
                          "\n 4 - выход")
                    es = input('Ввод: ')
                    es = re.sub(r'\D+', '', es)
                    if es == '1':
                        print('\n')
                        active_transfers_query = f""" SELECT * FROM history WHERE received_user_id = {id_query} AND status = 'active' LIMIT 2 """
                        cursor.execute(active_transfers_query)
                        result_query = cursor.fetchall()
                        if result_query:
                            for i in result_query:
                                print(f"ID: {i['id']}, Сумма: {i['summ']}, Страна: {i['country_id']}, Время отправления: {i['Time Send']}, Отправитель: {i['sender_user_id']}, Получатель: {i['received_user_id']}, Место получения: {i['received_point']}, Время получения: {i['Received_time']}, Статус: {i['status']}")
                        else:
                            print('На данный момент у вас нету активных переводов\n')
                    elif es == '2':
                        print('\nВведите айди АКТИВНОГО перевода')
                        trans_id = input('Ввод: ')
                        commit_transfers_query = f""" UPDATE history SET status = 'delivered' WHERE received_user_id = {id_query} AND id = {trans_id} AND status = 'active'""";
                        select_transfers_query = f""" SELECT * FROM history WHERE received_user_id = {id_query} AND id = {trans_id} AND status = 'active'"""
                        cursor.execute(commit_transfers_query)
                        result_query = cursor.fetchall()
                        connection.commit()
                        cursor.execute(select_transfers_query)
                        result_query = cursor.fetchall()
                        if result_query:
                            print('\n')
                            for i in result_query:
                                print(f"ID: {i['id']}, Сумма: {i['summ']}, Страна: {i['country_id']}, Время отправления: {i['Time Send']}, Отправитель: {i['sender_user_id']}, Получатель: {i['received_user_id']}, Место получения: {i['received_point']}, Время получения: {i['Received_time']}, Статус: {i['status']}")
                        else:
                            print('\nИспользован неверный айди или такого перевода на существует.')
                    elif es == '3':
                        print('\nВведите айди ПОЛУЧЕННОГО перевода')
                        trans_id = input('Ввод: ')
                        tax_transfers_query = f"""SELECT id, summ, country_id, CASE WHEN country_id = 3 THEN summ * 0.009 WHEN country_id = 2 THEN summ * 0.005 ELSE 0 END AS tax_rate FROM history WHERE received_user_id = {id_query} AND id = {trans_id} AND status = 'delivered'""";
                        cursor.execute(tax_transfers_query)
                        result_query = cursor.fetchall()
                        if result_query:
                            for i in result_query:
                                print(f"ID: {i['id']}, Страна: {i['country_id']}, Сумма: {i['summ']} , Сумма налогов: {i['tax_rate']}")
                        else:
                            print('\nИспользован неверный айди или это не ваш перевод или такого перевода на существует.')
                    elif es == '4':
                        print('\nДо свидания!')
                        print('\n')
                        break
                    else:
                        print('Неправильный ввод')
            else:
                print('\nНеверный логин или пароль'
                        '\nНажмите 1 что бы вернуться в начало'
                        '\nНажмите 2 что бы выйти')
                sp = input('Ввод: ')
                sp = re.sub(r'\D+', '', sp)
                if sp == '2':
                    print('\nДо свидания!')
                    break
                elif sp == '1':
                    print('\n')
                else:
                    print('Неправильный ввод')
except Exception as ex:
    print('Программа завершена с ошибками')
    print(ex)
finally:
    print('Программа завершена')
    connection.close