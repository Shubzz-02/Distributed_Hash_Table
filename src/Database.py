import os
import sqlite3
from sqlite3 import Error


class Database:
    """DATABASE RELATED WORK HERE"""

    def __init__(self, db_file, db_conn=None):
        self.db_file = db_file
        self.db_conn = db_conn
        pass

    def check_if_exist(self):
        try:
            if not os.path.exists(self.db_file):
                self.db_conn = sqlite3.connect(self.db_file)
                self.db_conn.execute('''CREATE TABLE FILES(
                ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                NAME TEXT NOT NULL,
                SHA TEXT NOT NULL UNIQUE,
                SIZE TEXT NOT NULL,
                PATH TEXT NOT NULL
                );''')
                print("Server --> Database CREATED")
                self.db_conn.commit()
            else:
                self.db_conn = sqlite3.connect(self.db_file)
                print("Server --> Database Already Exists")
        except Error as e:
            print(e)
        pass

    def insert(self, data):
        # self.db_conn.execute('''INSERT INTO FILES(NAME,SHA,SIZE,PATH)
        # VALUES ('zip','118B50C9E03B77F2A7311444FF6B01807E1C793905A2D693C97B18A335AD7475','2849963','../res/118B50C9E03B77F2A7311444FF6B01807E1C793905A2D693C97B18A335AD7475_IP_List.details'
        # );
        # ''')
        try:
            self.db_conn = sqlite3.connect(self.db_file)
            tdata = data.split(",")
            # print tdata  # ['118b50c9e03b77f2a7311444ff6b01807e1c793905a2d693c97b18a335ad7475', '2849963', 'zip']
            sql = '''INSERT INTO FILES(NAME,SHA,SIZE,PATH) VALUES (?,?,?,?);'''
            values = (tdata[2], tdata[0], tdata[1], "../res/" + tdata[0] + "_IP_List.details")
            self.db_conn.execute(sql, values)
            self.db_conn.commit()
            self.db_conn.close()
            print("Database --> Successfully inserted " + tdata[0])
        except Error as e:
            print("Database --> " + str(e))
        pass

    def get_det(self, det):
        path = ""
        try:
            db_conn = sqlite3.connect(self.db_file)
            data = db_conn.execute('''SELECT PATH from FILES WHERE SHA=?''', (det,))
            for row in data:
                path = row[0]
        except Error as e:
            print(str(e))
        return path
        pass
