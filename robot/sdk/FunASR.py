# -*- coding:utf-8 -*-
import librosa
from funasr import AutoModel
from robot import logging

logger = logging.getLogger(__name__)


# fun asr
class FunASR(object):
    model_dir = "iic/SenseVoiceSmall"
    
    def __init__(self):
        self.model = AutoModel(model="paraformer-zh",  vad_model="fsmn-vad", punc_model="ct-punc",
                  # spk_model="cam++"
                  )

    def asr(self, wav_file):
        sampleRate = 16000

        try:
            # speech, rate = librosa.load(wav_file, mono=True, sr=sampleRate)
            text = self.model.generate(input=wav_file, batch_size_s=300, hotword='魔搭')
            return text
        except Exception as err:
            logger.error(f"Fun ASR 处理失败: {err}", stack_info=True)