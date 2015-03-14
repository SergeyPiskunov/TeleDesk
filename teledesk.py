# -*- coding: utf-8 -*-
import sqlite3 as sqlite


class DBConnector():

    def __init__(self, db_file):
        self.db = sqlite.connect(db_file)

    def create_blank_base(self):
        pass

    def get_data(self, query):
        with self.db:
            cursor = self.db.execute(query)
            column_count = cursor.description.__len__()
            answer = []
            for row in cursor:
                record = {}
                for column in range(column_count):
                    record[cursor.description[column][0]] = row[column]
                answer.append(record)
            return answer

    def get_data_std(self, query):

        with self.db:
            self.db.row_factory = sqlite.Row
            cur = self.db.cursor()
            cur.execute(query)
            return cur.fetchall()


dbc = DBConnector("config.db")
data = dbc.get_data("SELECT * FROM FOLDERS")
print data[0]["Name"]
data = dbc.get_data_std("SELECT * FROM FOLDERS")
print data[0]["Name"]
