import time
from datetime import datetime
from ..Db.Mysql import Mysql


class Subscribers(Mysql):
    field_id = 0
    field_user_id = 1
    field_start = 2
    field_end = 3

    table = 'subscribers'

    def getUser(self, userId):
        connect = self.getConnect()
        cursor = self.getCursor(connect)
        try:
            cursor.execute(
                f'SELECT * FROM {self.table} where `user_id` = {userId} ORDER BY `id` DESC'
            )
            result = cursor.fetchone()
        except():
            result = None
        self.closeAll(connect, cursor)
        return result

    def addNewSubscriber(self, userId):
        connect = self.getConnect()
        cursor = self.getCursor(connect)
        try:
            startSubTime = datetime.utcfromtimestamp(time.time())
            endSubTime = datetime.utcfromtimestamp(time.time() + (30 * (60 * 60 * 24)))
            cursor.execute(
                f"INSERT INTO {self.table} (user_id, start_sub, end_sub) VALUES ({userId}, '{startSubTime}', '{endSubTime}')"
            )
        except():
            self.addNewSubscriber(userId)
        self.closeAll(connect, cursor)
