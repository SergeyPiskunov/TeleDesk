# -*- coding: utf-8 -*-
import sqlite3 as sqlite


class DBConnector(object):
    """ SQLite Database wrapper """

    def __init__(self, db_file):
        self.db_file = db_file
        self.db = sqlite.connect(db_file)

    def get_data(self, query, parameters=None):
        with self.db:
            self.db.row_factory = sqlite.Row
            cursor = self.db.cursor()
            if parameters:
                cursor.execute(query, (parameters,))
            else:
                cursor.execute(query)
            return cursor.fetchall()

    def execute(self, query, parameters=None, return_lastrow=None):
        with self.db:
            cursor = self.db.cursor()
            if parameters:
                cursor.execute(query, (parameters,))
            else:
                cursor.execute(query)
            self.db.commit()

            if return_lastrow:
                return cursor.lastrowid

if __name__ == "__main__":
        dbc = DBConnector("config.db")
        data = dbc.get_data("SELECT * FROM FOLDERS WHERE ID=?", '1')
        print data



