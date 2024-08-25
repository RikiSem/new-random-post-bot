# from ..Confs.DbConf import DbConf
from mysql.connector import connect, Error


class Mysql:
    def getConnect(self):
        connection = connect(
            user='root',
            password='',
            host='mysql',
            database='randomBot',
            ssl_disabled=True
        )
        connection.autocommit = True

        return connection

    def getCursor(self, connection):
        return connection.cursor(buffered=True)

    def closeAll(self, connection, cursor):
        connection.close()
        cursor.close()
