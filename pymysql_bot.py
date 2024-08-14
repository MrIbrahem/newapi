"""
from newapi import pymysql_bot
# result = pymysql_bot.sql_connect_pymysql(query, return_dict=False, values=None, main_args={}, credentials={}, conversions=None)
"""
import pymysql
import pymysql.cursors
import pkg_resources
import traceback
from newapi.except_err import exception_err
import pywikibot

def get_pymysql_version():
    py_v = pymysql.__version__.rstrip('.None')
    return pkg_resources.parse_version(py_v)

def sql_connect_pymysql(query, return_dict=False, values=None, main_args={}, credentials={}, conversions=None):
    args = main_args.copy()
    args["cursorclass"] = pymysql.cursors.DictCursor if return_dict else pymysql.cursors.Cursor
    if conversions:
        args["conv"] = conversions

    params = values or None  # Simplify condition

    try:
        connection = pymysql.connect(**args, **credentials)
    except Exception as e:
        exception_err(e)
        return []

    pymysql_version = get_pymysql_version()
    if pymysql_version < pkg_resources.parse_version("1.0.0"):
        from contextlib import closing
        connection = closing(connection)

    with connection as conn, conn.cursor() as cursor:

        # skip sql errors
        try:
            cursor.execute(query, params)

        except Exception as e:
            exception_err(e)
            return []

        try:
            results = cursor.fetchall()
        except Exception as e:
            exception_err(e)
            return []

    return results
