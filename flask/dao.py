import MySQLdb

class DAO:
    def __init__(self, username = 'root', password = '123456', dbname = 'blog'):
        self.username = username
        self.password = password
        self.dbname = dbname

    def connect(self):
        conn = MySQLdb.Connect(host='localhost', user=self.username, passwd=self.password, \
        db=self.dbname, charset="utf8", use_unicode="True")
        return conn

    def execute(self,sql):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
        finally:
            cur.close()
            conn.close()
