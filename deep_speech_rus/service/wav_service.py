import logging
import service.wavTranscriber as wavTranscriber
import numpy as np
from app import MODELS_PATH
from app import FILE_STORAGE

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


class WavService:
    def __init__(self):
        # Resolve all the paths of model files
        output_graph, scorer = wavTranscriber.resolve_models(MODELS_PATH)
        self.output_graph = output_graph
        self.scorer = scorer

        # Load output_graph, alpahbet and scorer
        self.model_retval = wavTranscriber.load_model(output_graph, scorer)

    def recognize(self, args):

        result = ''
        inference_time = 0.0

        # Run VAD on the input file
        wave_file = args['audio']
        segments, sample_rate, audio_length = wavTranscriber.vad_segment_generator(FILE_STORAGE + wave_file, args['aggressive'])

        for i, segment in enumerate(segments):
            # Run deepspeech on the chunk that just completed VAD
            logging.debug("Processing chunk %002d" % (i,))
            audio = np.frombuffer(segment, dtype=np.int16)
            output = wavTranscriber.stt(self.model_retval[0], audio, sample_rate)
            inference_time += output[1]
            logging.debug("Transcript: %s" % output[0])
            result += output[0] + ' '

        return result


component = WavService()
