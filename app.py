from flask import Flask, jsonify, render_template, render_template, request, send_file
from src.db.cafes import cafe_table_create, cafe_table_del, cafe_table_modify
from src.db.general import get_data_from_table, admin_password_correct
from src.globals import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html', error = None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != login_pwd and request.form['password'] != admin_pwd:
            error = 'Invalid Code.'
        elif request.form['password'] == admin_pwd:
            return render_template('admin_panel.html')
        else:
            return render_template('map.html')
    return render_template('login_prompt.html', error = error)

@app.route('/cafes', methods=['GET'])
def cafes():
    cafe_data = []
    if cafe_table_name:
        cafe_data = get_data_from_table(cafe_table_name)
    final_data = {"cafes" : cafe_data}
    return jsonify(
        final_data
    ), 200

@app.route('/create_cafe', methods=['POST', 'GET'])
def create_cafe():
    if admin_password_correct(request.json):
        if (not cafe_table_create(request.json)):
            return jsonify({"status" : "failed - some fields are empty"}), 400
    else:
        return jsonify({"status" : "failed - incorrect password"}), 400
    return jsonify(
            {"status" : "success"}
    ), 200

@app.route('/modify_cafe', methods=['POST', 'GET'])
def modify_cafe():
    if admin_password_correct(request.json):
        if (not cafe_table_modify(request.json)):
            return jsonify({"status" : "failed - some fields are empty"}), 400
    else:
        return jsonify({"status" : "failed - incorrect password"}), 400
    return jsonify({"status" : "success"}), 200

@app.route('/delete_cafe', methods=['POST', 'GET'])
def delete_cafe():
    if admin_password_correct(request.json):
        if (not cafe_table_del(request.json)):
            return jsonify({"status" : "failed - malformed request"}), 400
    else:
        return jsonify({"status" : "failed - incorrect password"}), 400
    return jsonify({"status" : "success"}), 200


@app.route('/toilets', methods=['GET'])
def toilets():
    toilet_data = []
    if (toilet_table_name):
        toilet_data = get_data_from_table(toilet_table_name) #type: ignore
    final_data = {"toilets" : toilet_data}
    return jsonify(final_data), 200

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')
