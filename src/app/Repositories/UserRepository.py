from ..Db.Mysql import Mysql


class UserRepository(Mysql):
    table = 'users'
    field_id = 0
    field_user_id = 1

    def isUserExist(self, userId):
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

    def getAllUsers(self):
        connect = self.getConnect()
        cursor = self.getCursor(connect)
        result = []
        try:
            cursor.execute(
                f'SELECT * FROM {self.table} WHERE 1'
            )
            result = cursor.fetchall()
        except():
            result = None
        self.closeAll(connect, cursor)

        return result

    def saveUser(self, userId, username):
        connect = self.getConnect()
        cursor = self.getCursor(connect)
        try:
            cursor.execute(
                f"INSERT INTO {self.table} (user_id, username) VALUES ({userId}, '{username}')"
            )
        except():
            self.saveUser(userId, username)
        self.closeAll(connect, cursor)
