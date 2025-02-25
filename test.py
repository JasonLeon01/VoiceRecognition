import sounddevice as sd
import numpy as np
import whisper

# 加载模型
model = whisper.load_model("turbo")

# 录制音频
def record_audio(duration=5, sample_rate=16000):
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return audio.flatten()

# 转换为文本
audio_data = record_audio()
result = model.transcribe(audio_data, language="zh")
print("识别结果:", result["text"])