#! /usr/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import sqlite3
from sqlite3 import Error
import errors

DATABASE = "cvt.db"
app = Flask(__name__)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

@app.route('/votes', methods=['POST'])
@auth.login_required
def create_vote():
    conn = create_connection(DATABASE)

    music_id = request.json['music_id']
    poll_id = request.json['poll_id']
    vote = (music_id, poll_id)

    sql = ''' INSERT INTO votes(music_id,poll_id)
                VALUES(?,?) '''

    cur = conn.cursor()
    cur.execute(sql, vote)
    conn.commit()

    vote_id = cur.lastrowid
    cur.execute('SELECT * FROM votes WHERE id=?', (vote_id,))
    vote = cur.fetchone()

    return jsonify(vote = vote)

@app.route('/votes')
def get():
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM votes')

    votes = cur.fetchall()

    return jsonify(votes = votes)

@app.route('/votes/<int:vote_id>')
@auth.login_required
def get_vote(vote_id):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM votes WHERE id=?', (vote_id,))

    vote = cur.fetchone()

    if len(vote) == 0:
        abort(404)

    return jsonify(vote = vote)

@app.route('/votes/<int:vote_id>', methods=['DELETE'])
def delete_vote(vote_id):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM votes WHERE id=?', (vote_id,))

    vote = cur.fetchone()

    if len(vote) == 0:
        abort(404)

    cur.execute('DELETE FROM votes WHERE id=?', (vote_id,))
    conn.commit()

    return jsonify({'Deleted': True})

if __name__ == '__main__':
    app.run(debug=True)
