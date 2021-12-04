import logging
import os

from pydub import AudioSegment

from app import FILE_STORAGE

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


# Service for file storage
class FileStorage:
    def __init__(self):
        pass

    # Save and convert file for model processing
    @staticmethod
    def save_file(file):
        filename = file.filename
        file.save(os.path.join(FILE_STORAGE, file.filename))

        if file.content_type == 'audio/mp3' or file.content_type == 'audio/mpeg':
            path = os.path.splitext(os.path.join(FILE_STORAGE, file.filename))[0] + ".wav"
            sound = AudioSegment.from_mp3(os.path.join(FILE_STORAGE, file.filename))
            sound.export(path, format="wav", parameters=['-ar', '16000', '-ac', '1', '-ab', '64'])
            os.remove(os.path.join(FILE_STORAGE, file.filename))
            filename = os.path.splitext(file.filename)[0] + ".wav"

        elif file.content_type == 'audio/ogg':
            path = os.path.splitext(os.path.join(FILE_STORAGE, file.filename))[0] + ".wav"
            sound = AudioSegment.from_ogg(os.path.join(FILE_STORAGE, file.filename))
            sound.export(path, format="wav", parameters=['-ar', '16000', '-ac', '1', '-ab', '64'])
            os.remove(os.path.join(FILE_STORAGE, file.filename))
            filename = os.path.splitext(file.filename)[0] + ".wav"

        return filename

    @staticmethod
    def rename_file(filename, new_name):
        os.rename(os.path.join(FILE_STORAGE, filename), os.path.join(FILE_STORAGE, new_name))

    @staticmethod
    def remove_file(filename):
        os.remove(os.path.join(FILE_STORAGE, filename))


component = FileStorage()
