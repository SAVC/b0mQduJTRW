import logging

from deeppavlov import configs, build_model

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


class TagService:
    def __init__(self):
        self.ner_model = build_model(configs.ner.ner_ontonotes_bert, download=True)

    def tags(self, text):
        return self.ner_model([text])


component = TagService()
