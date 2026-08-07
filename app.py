from flask import Flask, jsonify, render_template, render_template, request, send_file
from src.db_connector import cafe_table_create, cafe_table_del, cafe_table_modify, get_data_from_table
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
        if (not cafe_table_create(request.json)):
            return jsonify({"status" : "failed - some fields are empty"}), 400
    return jsonify(
            {"status" : "success"}
    ), 200

@app.route('/modify_cafe', methods=['POST', 'GET'])
def modify_cafe():
    if request.json is None or not ("password" in request.json) or request.json['password'] != admin_pwd:
        return jsonify({"status" : "failed - incorrect password"}), 400

    elif request.json['password'] == admin_pwd and cafe_table_name:
        if (not cafe_table_modify(request.json)):
            return jsonify({"status" : "failed - some fields are empty"}), 400
    return jsonify({"status" : "success"}), 200

@app.route('/delete_cafe', methods=['POST', 'GET'])
def delete_cafe():
    if request.json is None or not ("password" in request.json) or request.json['password'] != admin_pwd:
        return jsonify({"status" : "failed - malformed request"}), 400

    elif request.json['password'] == admin_pwd:
        if (not cafe_table_del(request.json)):
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
