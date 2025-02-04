import json
import numpy as np
from vosk import Model, KaldiRecognizer

# 录音参数
SAMPLERATE = 16000  # 采样率
CHANNELS = 1  # 单声道

recognition_model_path = "./vosk-model-cn-0.22"
recognition_model = Model(recognition_model_path)
recognizer = KaldiRecognizer(recognition_model, SAMPLERATE)

# 语音识别函数
def recognize_audio(audio_data):
    recognizer.Reset()
    recognizer.AcceptWaveform((audio_data * 32767).astype(np.int16).tobytes())
    result = recognizer.FinalResult()
    result_dict = json.loads(result)
    return result_dict.get("text", "").replace(" ", "")
