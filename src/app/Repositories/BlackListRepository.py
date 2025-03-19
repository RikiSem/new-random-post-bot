from ..Db.Mysql import Mysql


class BlackList(Mysql):
    field_id = 0
    field_user_id = 1

    table = 'blacklist'

    def getUser(self, userId):
        connect = self.getConnect()
        cursor = self.getCursor(connect)
        try:
            cursor.execute(
                f'SELECT * FROM {self.table} WHERE user_id = {userId}'
            )
            result = cursor.fetchone()
        except():
            result = None
        self.closeAll(connect, cursor)
        return result
    
    def blockUser(self, userId: int):
        connect = self.getConnect()
        cursor = self.getCursor(connect)
        try:
            cursor.execute(
                f'INSERT INTO {self.table} (user_id) VALUES ({userId})'
            )
        except():
            pass