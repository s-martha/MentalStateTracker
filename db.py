import psycopg2
from datetime import datetime, timedelta
import settings


def GetConnection():
    return psycopg2.connect(dbname=settings.DATABASE_NAME, user=settings.DATABASE_USERNAME,
                            password=settings.DATABASE_PASSWORD, host=settings.DATABASE_HOST)


def AddMood(user_id, mood_value):
    """Добавление в БД настроения пользователя и даты отметки настроения."""

    connection = GetConnection()
    cursor = connection.cursor()

    cursor.execute('''SELECT COUNT(*) from public."UsersMood";''')
    line_id = cursor.fetchall()[0][0] + 1

    cursor.execute(f'''INSERT INTO public."UsersMood"(id, user_id, mood, mark_date)
                   VALUES ({line_id}, {user_id}, {mood_value}, '{datetime.now().date()}');''')
    cursor.close()
    connection.commit()
    connection.close()


def GetMoodDatesAndValues(user_id, period):
    """Строит график настроения за указанный период. !Период времени! Не последние n отметок!
    В результате работы функция сохраняет изображение графика, которое будет отправлено пользователю.
    """

    connection = GetConnection()
    cursor = connection.cursor()

    if period == 'all_time':
        cursor.execute(f'''SELECT mood, mark_date FROM public."UsersMood"
                       WHERE (user_id = {user_id});''')
    else:  # days is a number of days
        query_date = datetime.now().date() - timedelta(days=period)
        cursor.execute(f'''SELECT mood, mark_date FROM public."UsersMood"
                       WHERE (user_id = {user_id} AND mark_date >= '{query_date}');''')

    response = cursor.fetchall()
    # print(response)

    cursor.close()
    connection.close()

    dates_val = dict()
    for mark in response:
        # print(mark)
        d = str(mark[1].day) if mark[1].day >= 10 else '0' + str(mark[1].day)
        m = str(mark[1].month) if mark[1].month >= 10 else '0' + str(mark[1].month)
        y = str(mark[1].year)[2:]
        # key = f'''{d}.{m}.{y}'''
        key = (y, m, d)
        dates_val[key] = dates_val.get(key, []) + [mark[0]]

    res = []
    for key in dates_val:
        res.append((key, sum(dates_val[key]) / len(dates_val[key])))
    res.sort()

    dates, values = [], []

    for key, val in res:
        key = f"{key[2]}.{key[1]}.{key[0]}"
        dates.append(key)
        values.append(val)

    return (dates, values)


def AddUserTime(user_id, user_time):
    print("AddUserTime:", user_id)

    connection = GetConnection()
    cursor = connection.cursor()
    cursor.execute(f'''SELECT form_time from public."UsersTime" WHERE user_id={user_id};''')
    response = cursor.fetchall()

    print("got response")

    if response == []:
        cursor.execute('''SELECT COUNT(*) from public."UsersTime";''')
        cursor.execute(f'''INSERT INTO public."UsersTime"(user_id, form_time)
                       VALUES ({user_id}, '{user_time}');''')
    else:
        cursor.execute(f'''UPDATE public."UsersTime" SET form_time='{user_time}'
                       WHERE user_id={user_id};''')

    cursor.close()
    connection.commit()
    connection.close()


def GetAllUsersInfo(user_time, users_weekly_stats):
    connection = GetConnection()
    cursor = connection.cursor()
    cursor.execute('''SELECT * from public."UsersTime";''')
    response = cursor.fetchall()
    cursor.close()
    connection.close()

    for line in response:
        if line[2]:  # сохраним время юзера, если он хочет получать формы
            h = str(line[1].hour) if line[1].hour >= 10 else '0' + str(line[1].hour)
            m = str(line[1].minute) if line[1].minute >= 10 else '0' + str(line[1].minute)
            user_time[line[0]] = f'''{h}:{m}'''
        if line[3]:
            users_weekly_stats.add(line[0])
