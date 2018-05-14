from flask import Flask, jsonify, abort, make_response, request
app = Flask(__name__)


users = [
    {
        'id': 1,
        'username': u'mc livinho',
        'song': u'fazer falta'
    },
    {
        'id': 2,
        'username': u'kevinho',
        'song': u'rabiola'
    }
]

@app.route('/users')
def get():
    return jsonify({'users': users})

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

@app.route('/users', methods=['POST'])
def post():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'username': request.json['username'],
        'song': request.json['song']
    }
    users.append(user)
    return jsonify({'user': user}), 201


@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)



if __name__ == '__main__':
    app.run(debug=True)
