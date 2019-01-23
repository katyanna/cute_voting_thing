#! /usr/bin/python
from flask import Flask, jsonify, request
import sqlite3
from sqlite3 import Error


DATABASE = "cvt.db"
app = Flask(__name__)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

@app.route('/polls', methods=['POST'])
def create_poll():
    conn = create_connection(DATABASE)

    begin_date = request.json['begin_date']
    end_date = request.json['end_date']
    music_a_id = request.json['music_a_id']
    music_b_id = request.json['music_b_id']
    user_id = request.json['user_id']

    poll = (begin_date, end_date, music_a_id, music_b_id, user_id)

    sql = ''' INSERT INTO polls(begin_date, end_date, music_a_id, music_b_id, user_id)
                VALUES(?, ?, ?, ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, poll)
    conn.commit()

    poll_id = cur.lastrowid
    cur.execute('SELECT * FROM polls WHERE id=?', (poll_id,))
    poll = cur.fetchone()

    return jsonify(poll = poll)

@app.route('/polls')
def get():
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM polls')

    polls = cur.fetchall()

    return jsonify(polls = polls)

@app.route('/polls/<int:poll_id>')
def get_poll(poll_id):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM polls WHERE id=?', (poll_id,))

    poll = cur.fetchone()

    if len(poll) == 0:
        abort(404)

    return jsonify(poll = poll)

@app.route('/polls/<int:poll_id>', methods=['PUT'])
def update_poll(poll_id):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM polls WHERE id=?', (poll_id,))

    poll = cur.fetchone()

    if len(poll) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'begin_date' in request.json and type(request.json['begin_date']) != str:
        abort(400)
    if 'end_date' in request.json and type(request.json['end_date']) != str:
        abort(400)
    if 'music_a_id' in request.json and type(request.json['music_a_id']) != str:
        abort(400)
    if 'music_b_id' in request.json and type(request.json['music_b_id']) != str:
        abort(400)
    if 'user_id' in request.json and type(request.json['user_id']) != str:
        abort(400)

    req_data = request.get_json()

    if 'begin_date' in req_data:
        begin_date = req_data['begin_date']
        cur.execute(' UPDATE polls SET begin_date = ? WHERE id = ?', (begin_date, poll_id,))
    if 'end_date' in req_data:
        end_date = req_data['end_date']
        cur.execute(' UPDATE polls SET end_date = ? WHERE id = ?', (end_date, poll_id,))
    if 'music_a_id' in req_data:
        music_a_id= req_data['music_a_id']
        cur.execute(' UPDATE polls SET music_a_id= ? WHERE id = ?', (music_a_id, poll_id,))
    if 'music_b_id' in req_data:
        music_b_id = req_data['music_b_id']
        cur.execute(' UPDATE polls SET music_b_id = ? WHERE id = ?', (music_b_id, poll_id,))
    if 'user_id' in req_data:
        user_id = req_data['user_id']
        cur.execute(' UPDATE polls SET user_id = ? WHERE id = ?', (user_id, poll_id,))
    conn.commit()

    cur.execute('SELECT * FROM polls WHERE id=?', (poll_id,))
    updated_poll = cur.fetchone()

    return jsonify(poll = updated_poll) 

@app.route('/polls/<int:poll_id>', methods=['DELETE'])
def delete_poll(poll_id):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM polls WHERE id=?', (poll_id,))

    poll = cur.fetchone()

    if len(poll) == 0:
        abort(404)

    cur.execute('DELETE FROM polls WHERE id=?', (poll_id,))
    conn.commit()

    return jsonify({'Deleted': True})

if __name__ == '__main__':
    app.run(debug=True)
