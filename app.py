from flask import Flask, jsonify, render_template, render_template, request, send_file
from psycopg import sql, connect as db_conn

from src.globals import *

app = Flask(__name__)

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

@app.route('/cafes', methods=['GET'])
def cafes():
    if cafe_table_name:
        cafe_data = get_data_from_table(cafe_table_name)
        final_data = {"cafes" : cafe_data}
        return jsonify(
            final_data
        ), 200
    else:
        return jsonify({"cafes" : []}), 400

@app.route('/create_cafe', methods=['POST', 'GET'])
def create_cafe():
    if request.json is None or not ("password" in request.json) or request.json['password'] != admin_pwd:
        return jsonify({"status" : "failed - incorrect password"}), 400

    elif request.json['password'] == admin_pwd and cafe_table_name:
        if "cafe" in request.json and all(key in request.json["cafe"] for key in ["name", "positionx", "positiony", "size", "coffee", "address", "price", "matcha", "chai", "notes"]):
            postgres_connection = db_conn(db_connection_string)
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
            return jsonify({"status" : "failed - some fields are empty"}), 400


    return jsonify(
            {"status" : "success"}
    ), 200

@app.route('/modify_cafe', methods=['POST', 'GET'])
def modify_cafe():
    if request.json is None or not ("password" in request.json) or request.json['password'] != admin_pwd:
        return jsonify({"status" : "failed - incorrect password"}), 400

    elif request.json['password'] == admin_pwd and cafe_table_name:
        if "cafe" in request.json and all(key in request.json["cafe"] for key in ["name", "positionx", "positiony", "size", "coffee", "address", "price", "matcha", "chai", "notes", "target"]):
            postgres_connection = db_conn(db_connection_string)
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
            return jsonify({"status" : "failed - some fields are empty"}), 400

    return jsonify({"status" : "success"}), 200

@app.route('/delete_cafe', methods=['POST', 'GET'])
def delete_cafe():
    if request.json is None or not ("password" in request.json) or request.json['password'] != admin_pwd:
        return jsonify({"status" : "failed - malformed request"}), 400

    elif request.json['password'] == admin_pwd:
        if "cafe" in request.json and "name" in request.json["cafe"] and cafe_table_name:
            postgres_connection = db_conn(db_connection_string)
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
