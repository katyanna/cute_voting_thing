from flask import Flask, jsonify, abort, make_response, request
app = Flask(__name__)


contestants = [
    {
        'id': 1,
        'mc': u'mc livinho',
        'song': u'fazer falta'
    },
    {
        'id': 2,
        'mc': u'kevinho',
        'song': u'rabiola'
    }
]

@app.route('/contestants')
def get():
    return jsonify({'contestants': contestants})

@app.route('/contestants/<int:contestant_id>')
def get_contestant(contestant_id):
    contestant = [contestant for contestant in contestants if contestant['id'] == contestant_id]
    if len(contestant) == 0:
        abort(404)
    return jsonify({'contestant': contestant[0]})

@app.route('/contestants', methods=['POST'])
def create_contestant():
    if not request.json or not 'mc' in request.json:
        abort(400)
    contestant = {
        'id': contestants[-1]['id'] + 1,
        'mc': request.json['mc'],
        'song': request.json['song']
    }
    contestants.append(contestant)
    return jsonify({'contestant': contestant}), 201

@app.route('/contestants/<int:contestant_id>', methods=['PUT'])
def update_contestant(contestant_id):
    contestant = [contestant for contestant in contestants if contestant['id'] == contestant_id]
    if len(contestant) == 0:
        abort(404)
    if not request.json:
        abort(400)
    contestant[0]['mc'] = request.json.get('mc', contestant[0]['mc'])
    contestant[0]['song'] = request.json.get('song', contestant[0]['song'])
    return jsonify({'contestant': contestant[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
