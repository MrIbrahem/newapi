"""

Usage:
# from newapi.db_bot import LiteDB
# db = LiteDB(db_path)
# db.create_table(table_name, fields, pk="id", **kwargs)
# db.show_tables(self)
# db.insert(table_name, data, check=True)
# db.get_data(table_name)
# db.select(table_name, args)

"""
# ---
import sqlite_utils


def tracer(sql, params):
    print("SQL: {} - params: {}".format(sql, params))


class LiteDB:
    def __init__(self, db_path):
        self.db_path = db_path
        # self.db = sqlite_utils.Database(db_path, tracer=tracer)
        self.db = sqlite_utils.Database(db_path)

    def create_table(self, table_name, fields, pk="id", **kwargs):
        # Create table if it doesn't exist
        self.db[table_name].create(fields, pk=pk, if_not_exists=True, ignore=True, **kwargs)

    def show_tables(self):
        tabs = self.db.table_names()
        for tab in tabs:
            print(f"Table: {tab}")
            print(f"schema: {self.db[tab].schema}")

    def insert(self, table_name, data, check=True):
        if check:
            is_in = self.select(table_name, data)
            if is_in:
                print(f" Skipping {data} - already in database")
                return

        self.db[table_name].insert(data, ignore=True, pk="id")

    def get_data(self, table_name):
        return self.db[table_name].rows

    def select(self, table_name, args):
        where = " and ".join([f"{k} = '{v}'" for k, v in args.items()])
        lista = []
        for row in self.db[table_name].rows_where(where):
            lista.append(row)
        return lista
