# -*- coding: utf-8 -*-
import sqlite3 as sqlite


class DBConnector(object):
    """ SQLite Database wrapper """
    def __init__(self, db_file):
        self.db = sqlite.connect(db_file)

    def get_data(self, query, parameters=None, return_collection=None):
        """ Reads data from the self.db database
            If return_collection=False returns only [0]-element of the query result list. """
        with self.db:
            self.db.row_factory = sqlite.Row
            cursor = self.db.cursor()
            cursor.execute(query, (parameters,))

            result = cursor.fetchall()
            if return_collection:
                return result
            else:
                if result:
                    return result[0]
                return []

    def execute(self, query, parameters=None, return_lastrow=None):
        """ Writes data to the self.db database.
            If return_lastrow=True returns ID of the appended row """
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




