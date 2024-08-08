from ..Db.Mysql import Mysql


class Subscribers(Mysql):
    field_id = 0
    field_user_id = 1
    field_start = 2
    field_end = 3

    table = 'subscribers'

    def getUser(self, userId):
        try:
            self.cursor.execute(
                f'SELECT * FROM {self.table} where user_id = {userId}'
            )
            result = self.cursor.fetchone()
        except():
            result = None
        return result
