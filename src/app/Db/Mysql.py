# from ..Confs.DbConf import DbConf
from mysql.connector import connect, Error


class Mysql:
    def __init__(self):
        try:
            self.mysql = connect(
                user='root',
                password='',
                host='mysql',
                database='randomBot'
            )
            self.cursor = self.mysql.cursor()
            self.mysql.autocommit = True
        except Error as e:
            print(e)