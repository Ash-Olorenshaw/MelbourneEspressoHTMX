from typing import Any

from src.globals import *
from psycopg import sql, connect as db_conn

def cafe_table_del(json_dat : Any) -> bool:
    if "cafe" in json_dat and "name" in json_dat["cafe"] and cafe_table_name:
        postgres_connection = db_conn(db_connection_string)
        postgres_cursor = postgres_connection.cursor()

        postgres_cursor.execute(sql.SQL('''DELETE FROM {} WHERE name = %s''').format(sql.Identifier(cafe_table_name)), [json_dat['cafe']['name']])
        postgres_cursor.close()
        postgres_connection.commit()
        postgres_connection.close()
        return True
    return False

def cafe_table_modify(json_dat : Any) -> bool:
    if "cafe" in json_dat and all(key in json_dat["cafe"] for key in ["name", "positionx", "positiony", "size", "coffee", "address", "price", "matcha", "chai", "notes", "target"]) and cafe_table_name:
        postgres_connection = db_conn(db_connection_string)
        postgres_cursor = postgres_connection.cursor()

        postgres_cursor.execute(
            sql.SQL('''UPDATE {} SET 
                (name, positionx, positiony, size, coffee, address, price, matcha, chai, notes)
                = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                WHERE name = %s''').format(sql.Identifier(cafe_table_name)), (
                    json_dat['cafe']['name'],
                    json_dat['cafe']['positionx'],
                    json_dat['cafe']['positiony'],
                    json_dat['cafe']['size'],
                    json_dat['cafe']['coffee'],
                    json_dat['cafe']['address'],
                    json_dat['cafe']['price'],
                    json_dat['cafe']['matcha'],
                    json_dat['cafe']['chai'],
                    json_dat['cafe']['notes'],
                    json_dat['cafe']['target']
                )
            )
        postgres_cursor.close()
        postgres_connection.commit()
        postgres_connection.close()
        return True
    return False

def cafe_table_create(json_dat : Any) -> bool:
    if "cafe" in json_dat and all(key in json_dat["cafe"] for key in ["name", "positionx", "positiony", "size", "coffee", "address", "price", "matcha", "chai", "notes"]) and cafe_table_name:
        postgres_connection = db_conn(db_connection_string)
        postgres_cursor = postgres_connection.cursor()

        postgres_cursor.execute(
            sql.SQL('''INSERT INTO {} 
                (name, positionx, positiony, size, coffee, address, price, matcha, chai, notes)
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''').format(sql.Identifier(cafe_table_name)), (
                    json_dat['cafe']['name'],
                    json_dat['cafe']['positionx'],
                    json_dat['cafe']['positiony'],
                    json_dat['cafe']['size'],
                    json_dat['cafe']['coffee'],
                    json_dat['cafe']['address'],
                    json_dat['cafe']['price'],
                    json_dat['cafe']['matcha'],
                    json_dat['cafe']['chai'],
                    json_dat['cafe']['notes']
                )
            )
        postgres_cursor.close()
        postgres_connection.commit()
        postgres_connection.close()
    else:
        return False
    return True

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
