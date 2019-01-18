#! /usr/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
import sqlite3
from sqlite3 import Error
import errors

DATABASE = "cvt.db"
app = Flask(__name__)
auth = HTTPBasicAuth()

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

@app.route('/musics', methods=['POST'])
#@auth.login_required
def create_music():
    conn = create_connection(DATABASE)

    title = request.json['title']
    artist = request.json['artist']
    music = (title, artist)

    sql = ''' INSERT INTO musics(title,artist)
                VALUES(?,?) '''

    cur = conn.cursor()
    cur.execute(sql, music)
    conn.commit()

    return jsonify(cur.lastrowid)

@app.route('/contestants')
def get():
    return jsonify({'contestants': [make_public_contestant(contestant) for contestant in contestants]})

@app.route('/contestants/<int:contestant_id>')
@auth.login_required
def get_contestant(contestant_id):
    contestant = [contestant for contestant in contestants if contestant['id'] == contestant_id]
    if len(contestant) == 0:
        abort(404)
    return jsonify({'contestant': [make_public_contestant(contestant[0])]})

@app.route('/contestants/<int:contestant_id>', methods=['PUT'])
@auth.login_required
def update_contestant(contestant_id):
    contestant = [contestant for contestant in contestants if contestant['id'] == contestant_id]
    if len(contestant) == 0:
        abort(404)
    if not request.json:
        abort(400)
    contestant[0]['mc'] = request.json.get('mc', contestant[0]['mc'])
    contestant[0]['song'] = request.json.get('song', contestant[0]['song'])
    return jsonify({'contestant': [make_public_contestant(contestant[0])]})

@app.route('/contestants/<int:contestant_id>', methods=['DELETE'])
@auth.login_required
def delete_contestant(contestant_id):
    contestant = [contestant for contestant in contestants if contestant['id'] == contestant_id]
    if len(contestant) == 0:
        abort(404)
    contestants.remove(contestant[0])
    return jsonify({'result': True})

def make_public_contestant(contestant):
    new_contestant = {}
    for field in contestant:
        if field == 'id':
            new_contestant['uri'] = url_for('get_contestant', contestant_id=contestant['id'], _external=True)
        else:
            new_contestant[field] = contestant[field]
    return new_contestant

@auth.get_password
def get_password(username):
    if username == 'fulano':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)

if __name__ == '__main__':
    app.run(debug=True)
