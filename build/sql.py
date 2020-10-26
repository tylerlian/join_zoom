import mysql.connector
from mysql.connector import Error
import sys

HOST = 'sql3.freemysqlhosting.net'
DATABASE = 'sql3372531'
USER = 'sql3372531'
PASSWORD = ''

def open_connection():
    connection = connect_sql()
    cursor = create_cursor(connection)
    return connection, cursor 

def close_connection(connection, cursor):
    connection.close()
    cursor.close()

def connect_sql():
    try:
        connection = mysql.connector.connect(host=HOST,
                                            database=DATABASE,
                                            user=USER,
                                            password=PASSWORD)
        return connection
    except Error as e: print("Error while connecting to MySQL", e)

def create_cursor(connection):
    try: return connection.cursor(buffered=True)
    except: print("Error creating cursor for connection.")

def create_table(connection, cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Zoom (id INT AUTO_INCREMENT PRIMARY KEY, class VARCHAR(255), zoom_id VARCHAR(255), link VARCHAR(255))")

def show_table(cursor, i):
    cursor.execute("SELECT * FROM Zoom")
    result = cursor.fetchall()
    print("List of all classes: ")
    for row in result: print(' | '.join(map(str, row[:i])))
    return len(result)

def join_classname(cursor, classname):
    cursor.execute("SELECT link FROM Zoom WHERE class LIKE " + classname)
    link = cursor.fetchone()
    return link[0] if link != None else None

def join_meeting(cursor, meeting):
    cursor.execute("SELECT link FROM Zoom WHERE zoom_id LIKE " + meeting)
    link = cursor.fetchone()
    return link[0] if link != None else None

def join_id(cursor, id):
    cursor.execute("SELECT link FROM Zoom WHERE id LIKE " + id)
    link = cursor.fetchone()
    return link[0] if link != None else None

def get_classname(cursor, meeting):
    cursor.execute("SELECT class FROM Zoom WHERE zoom_id LIKE " + meeting)
    zoom_id = cursor.fetchone()
    return zoom_id[0] if zoom_id != None else None

def get_meetingid(cursor, classname):
    cursor.execute("SELECT zoom_id FROM Zoom WHERE class LIKE " + classname)
    zoom_id = cursor.fetchone()
    return zoom_id[0] if zoom_id != None else None

def add_row(connection, cursor, classname, meeting, link):
    sql = 'INSERT INTO Zoom (class, zoom_id, link) VALUES (%s, %s, %s)'
    val = (classname, meeting, link)
    cursor.execute(sql, val)
    connection.commit()

def del_row(connection, cursor, search):
    temp = "'%" + search + "%'"
    if search.isdigit(): cursor.execute("DELETE FROM Zoom WHERE zoom_id LIKE " + temp)
    else: cursor.execute("DELETE FROM Zoom WHERE class LIKE " + temp)
    connection.commit()

def main(): # Delete table to reset sql table
    connection, cursor = open_connection()
    cursor.execute("DROP TABLE Zoom")
    create_table(connection, cursor)
    connection.commit()
    close_connection(connection, cursor)

if __name__ == '__main__':
    main()
