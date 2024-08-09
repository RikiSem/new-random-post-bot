from ..Db.Mysql import Mysql


class PostRepository(Mysql):

    field_id = 0
    field_type = 1
    field_entity_id = 2

    photo_type = 'photo'
    video_type = 'video'

    def savePost(self, type, entityId):
        self.cursor.execute(
            f"INSERT INTO post (type, entity_id) VALUES ('{type}', {entityId})"
        )

    def getLastPostByType(self, type):
        self.cursor.execute(
            f"SELECT * FROM post WHERE type = '{type}' ORDER BY id DESC"
        )
        post = self.cursor.fetchone()

        return post

