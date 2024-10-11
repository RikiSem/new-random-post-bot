from Confs.DbConf import DbConf
from Db.Mysql import Mysql

try:
    mysql = Mysql()
    connection = mysql.getConnect()
    cursor = mysql.getCursor(connection)
    query = "CREATE TABLE subscribers(" \
            "id INT AUTO_INCREMENT PRIMARY KEY, " \
            "user_id VARCHAR(255), " \
            "start CHAR(255), " \
            "end CHAR(255)" \
            ")"
    cursor.execute(query)

    query = "CREATE TABLE users(" \
        "id INT AUTO_INCREMENT PRIMARY KEY, " \
        "user_id VARCHAR(255), " \
        "username CHAR(255) " \
        ")"
    cursor.execute(query)

    query = "CREATE TABLE blacklist(" \
            "id INT AUTO_INCREMENT PRIMARY KEY, " \
            "user_id INT " \
            ")"
    cursor.execute(query)

    query = "CREATE TABLE post(" \
            "id INT AUTO_INCREMENT PRIMARY KEY, " \
            "type CHAR(255)," \
            "entity_id INT " \
            ")"
    cursor.execute(query)

    mysql.closeAll(connection, cursor)
except Exception as e:
    print(e)
