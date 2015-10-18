# -*- coding: utf-8 -*-
import sqlite3 as sqlite


class DBConnector(object):
    """ SQLite Database wrapper """
    def __init__(self, db_file, encrypted):
        self.db = sqlite.connect(db_file)
        if encrypted:
            self.db.text_factory = bytes

    def get_data(self, query, parameters=None, return_collection=None):
        """ Reads data from the self.db database
            If return_collection=False returns only [0]-element of the query result list. """
        with self.db:
            self.db.row_factory = sqlite.Row
            cursor = self.db.cursor()
            if parameters:
                cursor.execute(query, (parameters,))
            else:
                cursor.execute(query)

            #convert sqlite3Row to a list of dicts
            result_rows = cursor.fetchall()
            result_dict = []
            for result_row in result_rows:
                result_dict.append(dict(zip(result_row.keys(), result_row)))

            if return_collection:
                return result_dict
            else:
                if result_dict:
                    return result_dict[0]
                return []

    def execute(self, query, parameters=None, return_lastrow=None):
        """ Writes data to the self.db database.
            If return_lastrow=True returns ID of the appended row """
        with self.db:
            cursor = self.db.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            self.db.commit()

            if return_lastrow:
                return cursor.lastrowid

if __name__ == "__main__":
    dbc = DBConnector("config.db")




