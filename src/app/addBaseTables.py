from Confs.DbConf import DbConf
from Db.Mysql import Mysql

try:
    connection = Mysql().mysql
    cursor = connection.cursor()
    query = "CREATE TABLE subscribers(" \
            "id INT AUTO_INCREMENT PRIMARY KEY, " \
            "user_id INT, " \
            "start INT, " \
            "end INT" \
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

    cursor.close()
    connection.close()
except Exception as e:
    print(e)
