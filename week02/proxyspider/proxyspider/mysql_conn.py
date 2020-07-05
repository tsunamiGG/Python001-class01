# CREATE TABLE `ip` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `ip` varbinary(20) DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

import pymysql

dbInfo = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'pytest'
}


class ConnDB(object):
    def __init__(self, dbInfo):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']

    def insert_ip(self, ip):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db
        )

        cusor = conn.cursor()
        try:
            cusor.execute('insert into ip(ip) values("%s")' % ip)
            # 关闭游标
            cusor.close()
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        # 关闭数据库连接
        conn.close()
