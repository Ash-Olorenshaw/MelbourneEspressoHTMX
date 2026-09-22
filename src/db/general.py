from typing import Any

from src.globals import *
from psycopg import sql, connect as db_conn

def get_data_from_table(table_name : str):
    postgres_connection = db_conn(db_connection_string)
    postgres_cursor = postgres_connection.cursor()

    postgres_cursor.execute(sql.SQL('''SELECT * FROM {}''').format(sql.Identifier(table_name)))
    test_dat = postgres_cursor.fetchall()
    postgres_cursor.close()
    postgres_connection.close()

    new_dat = []
    for i, _ in enumerate(test_dat):
        new_dat.append(list(test_dat[i]))
        new_dat[i].pop(0)

    return new_dat

def admin_password_correct(req_json : Any | None):
    return req_json is not None and "password" in req_json and req_json['password'] == admin_pwd
