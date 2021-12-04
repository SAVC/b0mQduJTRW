class RecognitionFactory:
    def __init__(self):
        self.__urls = {
            'eng': 'http://localhost:5001/s2t',
            'rus': 'http://localhost:5002/s2t'
        }

    # Get recognition service url by model name
    def get_url(self, lang):
        return self.__urls[lang]

    # All models
    def get_models(self):
        return list(self.__urls.keys())

    # Aggressive levels
    @staticmethod
    def get_aggressive_levels():
        return [0, 1, 2, 3]


component = RecognitionFactory()
