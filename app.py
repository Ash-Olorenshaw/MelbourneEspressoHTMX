import sys
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, render_template, request, send_file
import psycopg
from psycopg import sql

load_dotenv()
app = Flask(__name__)

login_pwd = os.getenv("LOGIN_PWD")
admin_pwd = os.getenv("ADMIN_PWD")

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
        if request.form['password'] != f'{login_pwd}' and request.form['password'] != admin_pwd:
            error = 'Invalid Code.'
        elif request.form['password'] == admin_pwd:
            return render_template('admin_panel.html')
        else:
            return render_template('map.html')
    return render_template('login_prompt.html', error = error)

def get_data_from_table(table_name : str):
    #print(f"getting data from {table_name}", file = sys.stderr)
    postgres_connection = psycopg.connect(db_connection_string)
    postgres_cursor = postgres_connection.cursor()

    postgres_cursor.execute(sql.SQL('''SELECT * FROM {}''').format(sql.Identifier(table_name)))
    #colnames = [desc[0] for desc in postgres_cursor.description]
    test_dat = postgres_cursor.fetchall()
    postgres_cursor.close()
    postgres_connection.close()

    new_dat = []
    for i, _ in enumerate(test_dat):
        new_dat.append(list(test_dat[i]))
        new_dat[i].pop(0)

    #print(new_dat, file = sys.stderr)
    #print(colnames, file = sys.stderr)
    return new_dat

@app.route('/cafes', methods=['GET'])
def cafes():
    cafe_data = get_data_from_table(cafe_table_name) #type: ignore
    final_data = {"cafes" : cafe_data}
    return jsonify(
        final_data
    ), 200

@app.route('/create_cafe', methods=['POST', 'GET'])
def create_cafe():
    #print(f"modifying with data '{request.json}'", file = sys.stderr)
    if request.json == None or not ("password" in request.json) or request.json['password'] != admin_pwd:
        return jsonify({"status" : "failed - malformed request"}), 400

    elif request.json['password'] == admin_pwd:
        if "cafe" in request.json and all(key in request.json["cafe"] for key in ["name", "positionx", "positiony", "size", "coffee", "address", "price", "matcha", "chai", "notes"]):
            postgres_connection = psycopg.connect(db_connection_string)
            postgres_cursor = postgres_connection.cursor()

            postgres_cursor.execute(
                sql.SQL('''INSERT INTO {} 
                    (name, positionx, positiony, size, coffee, address, price, matcha, chai, notes)
                    VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''').format(sql.Identifier(cafe_table_name)), (
                        request.json['cafe']['name'],
                        request.json['cafe']['positionx'],
                        request.json['cafe']['positiony'],
                        request.json['cafe']['size'],
                        request.json['cafe']['coffee'],
                        request.json['cafe']['address'],
                        request.json['cafe']['price'],
                        request.json['cafe']['matcha'],
                        request.json['cafe']['chai'],
                        request.json['cafe']['notes']
                    )
                )
            postgres_cursor.close()
            postgres_connection.commit()
            postgres_connection.close()
        else:
            return jsonify({"status" : "failed - malformed request"}), 400


    return jsonify(
            {"status" : "success"}
    ), 200

@app.route('/modify_cafe', methods=['POST', 'GET'])
def modify_cafe():
    #print(f"modifying with data '{request.json}'", file = sys.stderr)
    if request.json == None or not ("password" in request.json) or request.json['password'] != admin_pwd:
        return jsonify({"status" : "failed - malformed request"}), 400

    elif request.json['password'] == admin_pwd:
        if "cafe" in request.json and all(key in request.json["cafe"] for key in ["name", "positionx", "positiony", "size", "coffee", "address", "price", "matcha", "chai", "notes", "target"]):
            postgres_connection = psycopg.connect(db_connection_string)
            postgres_cursor = postgres_connection.cursor()

            postgres_cursor.execute(
                sql.SQL('''UPDATE {} SET 
                    (name, positionx, positiony, size, coffee, address, price, matcha, chai, notes)
                    = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    WHERE name = %s''').format(sql.Identifier(cafe_table_name)), (
                        request.json['cafe']['name'],
                        request.json['cafe']['positionx'],
                        request.json['cafe']['positiony'],
                        request.json['cafe']['size'],
                        request.json['cafe']['coffee'],
                        request.json['cafe']['address'],
                        request.json['cafe']['price'],
                        request.json['cafe']['matcha'],
                        request.json['cafe']['chai'],
                        request.json['cafe']['notes'],
                        request.json['cafe']['target']
                    )
                )
            postgres_cursor.close()
            postgres_connection.commit()
            postgres_connection.close()
        else:
            return jsonify({"status" : "failed - malformed request"}), 400

    return jsonify({"status" : "success"}), 200

@app.route('/delete_cafe', methods=['POST', 'GET'])
def delete_cafe():
    if request.json == None or not ("password" in request.json) or request.json['password'] != admin_pwd:
        return jsonify({"status" : "failed - malformed request"}), 400

    elif request.json['password'] == admin_pwd:
        if "cafe" in request.json and "name" in request.json["cafe"]:
            postgres_connection = psycopg.connect(db_connection_string)
            postgres_cursor = postgres_connection.cursor()

            postgres_cursor.execute(sql.SQL('''DELETE FROM {} WHERE name = %s''').format(sql.Identifier(cafe_table_name)), [request.json['cafe']['name']])
            postgres_cursor.close()
            postgres_connection.commit()
            postgres_connection.close()
        else:
            return jsonify({"status" : "failed - malformed request"}), 400

    return jsonify({"status" : "success"}), 200


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
