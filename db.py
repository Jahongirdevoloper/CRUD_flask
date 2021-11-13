import psycopg2
from psycopg2._psycopg import Error

class Db:
    def __init__(self,database="crud", user="postgres", password="1234", host="127.0.0.1", port="5432"):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
    def __enter__(self):
        try:
            self.con = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
            self.cur = self.con.cursor()
            return self.cur
        except (Error, Exception) as e:
            print(e)
    
    def __exit__(self,exc_type, exc_val, exc_tb):
        if self.con:
            self.con.commit()
            self.cur.close()
            self.con.close()