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
@auth.login_required
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

    music_id = cur.lastrowid
    cur.execute('SELECT * FROM musics WHERE id=?', (music_id,))
    music = cur.fetchone()

    return jsonify(music = music)

@app.route('/musics')
def get():
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM musics')

    musics = cur.fetchall()

    return jsonify(musics = musics)

@app.route('/musics/<int:music_id>')
@auth.login_required
def get_music(music_id):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM musics WHERE id=?', (music_id,))

    music = cur.fetchone()

    if len(music) == 0:
        abort(404)

    return jsonify(music = music)

@app.route('/musics/<int:music_id>', methods=['PUT'])
@auth.login_required
def update_music(music_id):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM musics WHERE id=?', (music_id,))

    music = cur.fetchone()

    if len(music) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'artist' in request.json and type(request.json['artist']) != str:
        abort(400)

    req_data = request.get_json()

    if 'title' in req_data:
        title = req_data['title']
        cur.execute(' UPDATE musics SET title = ? WHERE id = ?', (title, music_id,))
    if 'artist' in req_data:
        artist = req_data['artist']
        cur.execute(' UPDATE musics SET artist = ? WHERE id = ?', (artist, music_id,))
    conn.commit()

    cur.execute('SELECT * FROM musics WHERE id=?', (music_id,))
    updated_music = cur.fetchone()

    return jsonify(music = updated_music) 

@app.route('/musics/<int:music_id>', methods=['DELETE'])
@auth.login_required
def delete_music(music_id):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM musics WHERE id=?', (music_id,))

    music = cur.fetchone()

    if len(music) == 0:
        abort(404)

    cur.execute('DELETE FROM musics WHERE id=?', (music_id,))
    conn.commit()

    return jsonify({'Deleted': True})

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
