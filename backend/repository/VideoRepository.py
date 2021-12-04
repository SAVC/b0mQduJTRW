from domain.Base import session_factory
from domain.VideoEntity import VideoEntity


class VideoRepository:
    def __init__(self):
        self.session = session_factory()

    def __del__(self):
        self.session.close()

    def save(self, video):
        self.session.add(video)
        self.session.commit()

    def get_all(self):
        return self.session.query(VideoEntity).all()

    def get(self, id):
        return self.session.query(VideoEntity).get(id)

    def delete(self, id):
        entity = self.session.query(VideoEntity).get(id)
        self.session.delete(entity)
        self.session.commit()

    def update_content(self, id, text):
        lecture = self.session.query(VideoEntity).get(id)
        lecture.content = text
        self.session.commit()


component = VideoRepository()
