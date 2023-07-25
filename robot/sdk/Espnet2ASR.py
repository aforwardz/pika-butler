# -*- coding:utf-8 -*-
import librosa
from robot.pks.espnet2.bin.asr_inference import Speech2Text
from robot import logging

logger = logging.getLogger(__name__)

# Espnet2 asr
class Espnet2ASR(object):
    def __init__(self):
        self.model = Speech2Text.from_pretrained("espnet/pengcheng_guo_wenetspeech_asr_train_asr_raw_zh_char")

    def asr(self, wav_file):
        sampleRate = 16000

        try:
            speech, rate = librosa.load(wav_file, mono=True, sr=sampleRate)
            text, *_ = self.model(speech)[0]
            return text
        except Exception as err:
            logger.error(f"Espnet2 ASR 处理失败: {err}", stack_info=True)
