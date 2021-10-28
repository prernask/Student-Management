import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = "system"
DATABASE = "students"


def get_database():
    try:
        database = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
        cursor = database.cursor(dictionary=True)
        cursor.execute("USE " + DATABASE)
        return database, cursor
    except mysql.connector.Error as err:
        if err.errno == 1049:
            print("Database does not exist so trying to create it...")
            try:
                cursor.execute("CREATE DATABASE "+DATABASE)
                cursor.execute("USE " + DATABASE)
            except mysql.connector.Error as err:
                return None, None
        return database,cursor
