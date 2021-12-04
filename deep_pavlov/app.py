import json
import logging

from flask import Flask, request

from serivice import *

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = Flask(__name__)

# HOST = '119.81.242.108'
HOST = '127.0.0.1'
PORT = 5500


# Echo route
@app.route('/health', methods=['GET'])
def echo():
    return 'alive'


# Get speech2text
@app.route('/tags', methods=['POST'])
def tags():
    request_dto = json.loads(request.data)
    return json.dumps(tag_service.tags(request_dto['text']))


# System shutdown route
@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
