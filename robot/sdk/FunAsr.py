# -*- coding:utf-8 -*-
import librosa
from funasr import AutoModel
from robot import logging

logger = logging.getLogger(__name__)


# fun asr
class FunAsr(object):
    model_dir = "iic/speech_paraformer_asr_nat-zh-cn-16k-common-vocab8358-tensorflow1"
    
    def __init__(self):
        self.model = AutoModel(model=self.model_dir, device="cuda:0", punc_model="ct-punc")

    def asr(self, wav_file):
        sampleRate = 16000

        try:
            # speech, rate = librosa.load(wav_file, mono=True, sr=sampleRate)
            res = self.model.generate(input=wav_file, batch_size_s=300, hotword='魔搭')
            text = ''
            if res:
                text = res[0].get('text', '')
            return text
        except Exception as err:
            logger.error(f"Fun ASR 处理失败: {err}", stack_info=True)