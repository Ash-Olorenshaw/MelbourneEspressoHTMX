import sys
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, render_template, request, send_file
import psycopg
from psycopg import sql

load_dotenv()
app = Flask(__name__)

login_pwd = os.getenv("LOGIN_PWD")

cafe_table_name = os.getenv("CAFE_TABLE")
toilet_table_name = os.getenv("TOILET_TABLE")

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pwd = os.getenv("DB_PWD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_connection_string = f"dbname={db_name} user={db_user} password={db_pwd} host={db_host} port={db_port}"

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html', error = None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['password'] != f'{login_pwd}':
            error = 'Invalid Code.'
        else:
            return render_template('map.html')
    return render_template('login_prompt.html', error = error)

def get_data_from_table(table_name : str):
    print(f"getting data from {table_name}", file = sys.stderr)
    postgres_connection = psycopg.connect(db_connection_string)
    postgres_cursor = postgres_connection.cursor()

    postgres_cursor.execute(sql.SQL('''SELECT * FROM {}''').format(sql.Identifier(table_name)))
    test_dat = postgres_cursor.fetchall()
    postgres_cursor.close()
    postgres_connection.close()

    new_dat = []
    for i, _ in enumerate(test_dat):
        new_dat.append(list(test_dat[i]))
        new_dat[i].pop(0)

    print(new_dat, file = sys.stderr)
    return new_dat

@app.route('/cafes', methods=['GET'])
def cafes():
    cafe_data = get_data_from_table(cafe_table_name) #type: ignore
    final_data = {"cafes" : cafe_data}
    return jsonify(
        final_data
    ), 200

@app.route('/toilets', methods=['GET'])
def toilets():
    toilet_data = get_data_from_table(toilet_table_name) #type: ignore
    final_data = {"toilets" : toilet_data}
    return jsonify(
        final_data
    ), 200

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')
