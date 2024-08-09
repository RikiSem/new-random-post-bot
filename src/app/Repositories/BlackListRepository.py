from ..Db.Mysql import Mysql


class BlackList(Mysql):

    field_id = 0
    field_user_id = 1

    table = 'blacklist'

    def getUser(self, userId):
        try:
            self.cursor.execute(
                f'SELECT * FROM {self.table} WHERE user_id = {userId}'
            )
            result = self.cursor.fetchone()
        except():
            result = None
        return result