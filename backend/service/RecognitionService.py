import json
import logging

import requests

from domain import AlchemyEncoder
from domain import VideoEntity
from repository import *
from service import recognition_factory

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


# Service for sending file to model and saving result
class ProcessingService:
    def __init__(self):
        pass

    @staticmethod
    def process(filename, lang, aggressive):
        result = {}
        response = ProcessingService.__recognize(filename, lang, aggressive)
        video = VideoEntity(filename, filename, response.text)
        video_repository.save(video)
        result['text'] = response.text
        result['id'] = video.id
        return result

    @staticmethod
    def get_videos():
        result = []
        for video in video_repository.get_all():
            result.append(json.loads(json.dumps(video, cls=AlchemyEncoder)))

        return json.dumps(result)

    @staticmethod
    def get_videos_headers():
        result = []
        for video in video_repository.get_all():
            video = json.loads(json.dumps(video, cls=AlchemyEncoder))
            video['content'] = ''
            result.append(video)

        return json.dumps(result)

    @staticmethod
    def get_video(id):
        return json.dumps(video_repository.get(id), cls=AlchemyEncoder)

    @staticmethod
    def get_video_text(id):
        return video_repository.get(id).content

    @staticmethod
    def delete_video(id):
        video_repository.delete(id)

    @staticmethod
    def update_video(id, json):
        video_repository.update_content(id, json['text'])

    @staticmethod
    def __recognize(filename, lang, aggressive):
        # sending get request and saving the response as response object
        payload = "{\t\n\t\"audio\":  \"" + filename + "\",\n\t\"aggressive\": " + aggressive + "\n\n}"
        headers = {'content-type': "application/json"}

        return requests.request("POST", recognition_factory.get_url(lang),
                                data=payload,
                                headers=headers)


component = ProcessingService()
