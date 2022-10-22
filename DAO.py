import datetime
import sqlite3

first_element = 0

def conn() -> sqlite3:
    try:
        sqlite_connection = sqlite3.connect('db/df_message.db')
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        return sqlite_connection

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


def save_data(message='test', chat_id=112233, status="не выучено"):
    date_time = str(datetime.datetime.now()).split('.')[first_element]
    sql = conn()
    cur = sql.cursor()
    try:
        cur.execute("INSERT INTO messages VALUES (?,?,?,?)", (message, chat_id, date_time, status))
        sql.commit()
        sql.close()
        print("данные успешно сохранены")
    except sqlite3.Error as error:
        print('что-то пошло не так', error)
        sql.close()


def get_all():
    sql = conn()
    cur = sql.cursor()
    try:
        result_set = cur.execute('SELECT * FROM messages').fetchall()
        sql.close()
        print("данные успешно получены")
        return result_set
    except sqlite3.Error as error:
        print('что-то пошло не так', error)
        sql.close()

def get_not_learned():
    sql = conn()
    cur = sql.cursor()
    try:
        result_set = cur.execute("SELECT rowid, message,chat_id,date_time,status FROM messages WHERE status = 'не выучено'").fetchall()
        sql.close()
        print("данные успешно получены")
        return result_set
    except sqlite3.Error as error:
        print('что-то пошло не так', error)
        sql.close()

def get_added():
    sql = conn()
    cur = sql.cursor()
    try:
        result_set = cur.execute("SELECT rowid,message,chat_id,date_time,status FROM messages WHERE status = 'выучено';").fetchall()
        sql.close()
        print("данные успешно получены")
        return result_set
    except sqlite3.Error as error:
        print('что-то пошло не так', error)
        sql.close()

def revert_status(message):
    sql = conn()
    cur = sql.cursor()
    try:
        cur.execute(f"UPDATE messages SET status = 'выучено' WHERE message = '{message}';")
        result_set = ''
        sql.commit()
        sql.close()
        return "статус успешно обновлен"
    except sqlite3.Error as error:
        print('что-то пошло не так', error)
        sql.close()

if __name__ == '__main__':
    try:
        sqlite_connection = sqlite3.connect('db/df_message.db')
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        sqlite_create_table_query = '''CREATE TABLE messages (
                                                message TEXT NOT NULL,
                                                chat_id TEXT NOT NULL,
                                                date_time TEXT NOT NULL,
                                                status TEXT NOT NULL);'''

        cursor.execute(sqlite_create_table_query)
    except Exception as  err:
        print(err)