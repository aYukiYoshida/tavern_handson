# -*- coding: utf-8 -*-

import datetime
import functools
import os
import sqlite3
import sys

import jwt
from flask import Flask, jsonify, request, g
import yaml

with open('/usr/local/authentication.yaml', 'r') as file:
    variables = yaml.safe_load(file)['variables']
    USER_NAME = variables['user']['username']
    PASSWORD = variables['user']['password']
    SERVER_NAME = variables['server']['name']
    SECRET = variables['server']['secret']

DATABASE = '/tmp/db'
app = Flask(__name__)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

        with db:
            try:
                db.execute(
                    "CREATE TABLE numbers_table (name TEXT NOT NULL, number INTEGER NOT NULL)"
                )
            except Exception:
                pass

    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route('/')
def root():
    return jsonify({'message': 'It works !!'}), 200


@app.route('/login', methods=['POST'])
def login():
    r = request.get_json()

    if r['username'] != USER_NAME or r['password'] != PASSWORD:
        return jsonify({'error': 'Incorrect username/password'}), 401

    payload = {
        'sub': USER_NAME,
        'aud': SERVER_NAME,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }

    token = jwt.encode(payload, SECRET, algorithm='HS256')

    return jsonify({'token': token})


def requires_jwt(endpoint):
    ''' Makes sure a jwt is in the request before accepting it '''

    @functools.wraps(endpoint)
    def check_auth_call(*args, **kwargs):
        token = request.headers.get('Authorization')

        # check token is present
        if not token:
            return jsonify({'error': 'No token'}), 401

        token_type, token = token.split(' ')

        if token_type.lower() != 'bearer':
            return jsonify({'error': 'Wrong token type'}), 401

        try:
            jwt.decode(token, SECRET, audience=SERVER_NAME,
                       algorithms=['HS256'])
        except:
            return jsonify({'error': 'Invalid token'}), 401

        return endpoint(*args, **kwargs)

    return check_auth_call


@app.route("/ping", methods=["GET"])
@requires_jwt
def ping():
    return jsonify({"data": "pong"}), 200


@app.route("/hello/<name>", methods=["GET"])
@requires_jwt
def hello(name):
    return jsonify({"data": "Hello, {}".format(name)}), 200


@app.route("/numbers", methods=["POST"])
@requires_jwt
def add_number():
    r = request.get_json()

    try:
        r["number"]
        r["name"]
    except (KeyError, TypeError):
        return jsonify({"error": "missing key"}), 400

    db = get_db()

    with db:
        db.execute("INSERT INTO numbers_table VALUES (:name, :number)", r)

    return jsonify({}), 201


@app.route("/numbers", methods=["GET"])
@requires_jwt
def get_number():
    r = request.args

    try:
        r["name"]
    except (KeyError, TypeError):
        return jsonify({"error": "missing key"}), 400

    db = get_db()

    with db:
        row = db.execute(
            "SELECT number FROM numbers_table WHERE name IS :name", r)

    try:
        number = next(row)[0]
    except StopIteration:
        return jsonify({"error": "Unknown number"}), 404

    return jsonify({"number": number})


@app.route("/double", methods=["POST"])
@requires_jwt
def double_number():
    r = request.get_json()

    try:
        r["name"]
    except (KeyError, TypeError):
        return jsonify({"error": "no number passed"}), 400

    db = get_db()

    with db:
        db.execute(
            "UPDATE numbers_table SET number = number*2 WHERE name IS :name", r)
        row = db.execute(
            "SELECT number FROM numbers_table WHERE name IS :name", r)

    try:
        double = next(row)[0]
    except StopIteration:
        return jsonify({"error": "Unknown number"}), 404

    return jsonify({"number": double})


@app.route("/reset", methods=["POST"])
def reset_db():
    db = get_db()

    with db:
        db.execute("DELETE FROM numbers_table")

    return "", 204


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred.', 500


if __name__ == '__main__':
    sys.exit(app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)),
                     debug=True))
