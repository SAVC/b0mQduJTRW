import json
import logging
from io import BytesIO

from flask import Flask, request, render_template, send_from_directory, send_file

from service import *

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = Flask(__name__)

# HOST = '119.81.242.108'
HOST = '127.0.0.1'
PORT = 5000
FILE_STORAGE = './filestorage/'


# Static content routes
@app.route('/')
def render_static():
    return render_template('index.html')


@app.route('/video-list')
def render_videos():
    return render_template('video.html')


@app.route('/editor/<id>')
def render_editor(id):
    return render_template('editor.html', value=str(id))


@app.route('/<path:path>')
def send_css(path):
    s = path.split('/')
    folder = ''
    i = 0
    for index in range(len(s)):
        folder += s[index] + '/'
        i = index
    filename = s[i]

    return send_from_directory(folder, filename)


# Echo route
@app.route('/health', methods=['GET'])
def echo():
    return 'alive'


@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']
    filename = file_storage.save_file(file)
    result = recognition_service.process(filename, request.form['lang'], request.form['aggressive'])
    file_storage.rename_file(filename, str(result['id']) + ".wav")
    return json.dumps(result)


@app.route("/lectures-head", methods=['GET'])
def lectures_head():
    return recognition_service.get_lectures_headers()


@app.route("/lectures", methods=['GET'])
def lectures():
    return recognition_service.get_lectures()


@app.route("/lectures/<id>", methods=['GET'])
def get_lecture(id):
    return recognition_service.get_lecture(id)


@app.route("/lecture/<id>", methods=['DELETE'])
def delete_lecture(id):
    recognition_service.delete_video(id)
    file_storage.remove_file(id + ".wav")


@app.route("/lecture/<id>", methods=['PUT'])
def update_lecture(id):
    recognition_service.update_lecture(id, json.loads(request.data))


@app.route("/aggressive/levels", methods=['GET'])
def aggressive_levels():
    return json.dumps(recognition_factory.get_aggressive_levels())


@app.route("/models", methods=['GET'])
def models():
    return json.dumps(recognition_factory.get_models())


@app.route('/download/<id>', methods=['GET'])
def test_download(id):
    lecture = recognition_service.get_video_text(id)
    # Use BytesIO instead of StringIO here.
    buffer = BytesIO()
    buffer.write(bytes(lecture, 'utf-8'))
    # Or you can encode it to bytes.
    # buffer.write('Just some letters.'.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True,
                     attachment_filename='lecture.txt',
                     mimetype='text/txt')


@app.route('/audio/<id>', methods=['GET'])
def audio(id):
    return send_from_directory(FILE_STORAGE, str(id) + ".wav")


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
