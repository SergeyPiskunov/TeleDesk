# -*- coding: utf-8 -*-

import sqlite3 as sqlite

class DBConnector():
    """ Database wrapper """

    def __init__(self, db_file):
        self.db = sqlite.connect(db_file)

    def create_blank_base(self):
        pass

    def get_data(self, query, parameters=None):

        with self.db:
            self.db.row_factory = sqlite.Row
            cursor = self.db.cursor()
            if parameters:
                cursor.execute(query, (parameters,))
            else:
                cursor.execute(query)
            return cursor.fetchall()

    def execute(self, query, parameters=None):
        with self.db:
            cursor = self.db.cursor()
            if parameters:
                cursor.execute(query, (parameters,))
            else:
                cursor.execute(query)
            self.db.commit()

if __name__ == "__main__":
    dbc = DBConnector("config.db")
    data = dbc.get_data("SELECT * FROM FOLDERS WHERE ID=?", '1')
    print data
    data = dbc.get_data("SELECT * FROM FOLDERS WHERE ID=:G", {'G': '1'})
    print data
    data = dbc.get_data("SELECT * FROM FOLDERS")
    print data


