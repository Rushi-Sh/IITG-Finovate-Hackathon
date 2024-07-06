from flask import Flask, request, jsonify
from Youtube import Recommender

app = Flask(__name__)

@app.route('/youtube', methods=['POST'])
def handle():
    data1 = request.get_json()

    if 'keywords' not in data1:
        return jsonify({'error': 'Keywords parameter is missing'}), 400
    
    keywords = data1['keywords']

    # Call Recommender function to get response
    response = Recommender(keywords)

    return jsonify({
        'keywords': keywords,
        'urls': response
    })

if __name__ == '__main__':
    app.run(debug=True, port=5002)
