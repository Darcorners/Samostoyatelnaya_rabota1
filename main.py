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
            Autorisation_query = f""" SELECT id FROM client WHERE '{login}' = login AND '{password}' = password """
            cursor.execute(Autorisation_query)
            id_query = cursor.fetchone()
            if id_query != None:
                id_query = id_query["id"]
                print(f'Авторизация успешна, ваш айди: {id_query}')
                while True:
                    print("Выберите действие: "
                          "\n 1 - отобразить 2 активных на данный момент перевода"
                          "\n 2 - подтвердить перевод"
                          "\n 3 - рассчитать сумму налогов доставленного перевода"
                          "\n 4 - выход")
                    es = int(input('Ввод: '))
                    if es == 1:
                        active_transfers_query = f""" SELECT * FROM history WHERE received_iser_id = {id_query} AND status = 'active' LIMIT 2 """
                        cursor.execute(active_transfers_query)
                        result_query = cursor.fetchall()
                        if result_query:
                            for i in result_query:
                                print(f"ID: {i['id']} Сумма: {i['count']} Страна: {i['country_id']} Отправитель: {i['sender_user_id']} Получатель: {i['received_iser_id']} Получение: {i['received_point']} Статус: {i['status']}")
                        else:
                            print('На данный момент у вас нету активных переводов')
                    elif es == 2:
                        print('Введите айди АКТИВНОГО перевода')
                        trans_id = int(input())
                        commit_transfers_query = f""" UPDATE history SET status = 'delivered' WHERE received_iser_id = {id_query} AND id = {trans_id} AND status = 'active' """
                        select_transfers_query = f""" SELECT * FROM history WHERE received_iser_id = {id_query} AND id = {trans_id}"""
                        cursor.execute(commit_transfers_query)
                        cursor.execute(select_transfers_query)
                        result_query = cursor.fetchall()
                        connection.commit()
                        if result_query:
                            print(result_query)
                        else:
                            print('Использован неверный айди.')
                    elif es == 3:
                        print('Введите айди ДОСТАВЛЕННОГО перевода')
                        trans_id = input()
                        tax_transfers_query = f""" SELECT id, count, CASE WHEN country_id = 2 THEN count * 0.005 WHEN country_id = 3 THEN count * 0.009 ELSE 0 END AS tax_rate FROM history WHERE received_iser_id = {id_query} AND id = {trans_id} AND status = 'delivered' ;"""
                        cursor.execute(tax_transfers_query)
                        result_query = cursor.fetchall()
                        connection.commit()
                        if result_query:
                            print(result_query)
                        else:
                            print('Использован неверный айди.')
                    elif es == 4:
                        print('До свидания!')
                        break
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