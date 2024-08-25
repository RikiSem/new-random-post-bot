from ..Db.Mysql import Mysql


class PostRepository(Mysql):

    field_id = 0
    field_type = 1
    field_entity_id = 2

    photo_type = 'photo'
    video_type = 'video'

    def savePost(self, type, entityId):
        connect = self.getConnect()
        cursor = self.getCursor(connect)
        cursor.execute(
            f"INSERT INTO post (type, entity_id) VALUES ('{type}', {entityId})"
        )

        cursor.close()
        connect.close()

    def getFirstPostByType(self, type):
        try:
            connect = self.getConnect()
            cursor = self.getCursor(connect)
            cursor.execute(
                f"SELECT * FROM post WHERE type = '{type}' ORDER BY id ASC"
            )
            post = cursor.fetchone()
            self.closeAll(connect, cursor)
            return post
        except():
            self.getLastPostByType(type)


    def getLastPostByType(self, type):
        try:
            connect = self.getConnect()
            cursor = self.getCursor(connect)
            cursor.execute(
                f"SELECT * FROM post WHERE type = '{type}' ORDER BY id DESC"
            )
            post = cursor.fetchone()
            self.closeAll(connect, cursor)
            return post
        except():
            self.getLastPostByType(type)

