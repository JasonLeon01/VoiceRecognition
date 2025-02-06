import os
import sys
import numpy as np
import torchaudio
import time
sys.path.append(os.path.join(os.getcwd(), 'Resemblyzer'))
from Resemblyzer.resemblyzer import preprocess_wav
import denoise
import record
import voiceprint
import recognise

# 录音参数
SAMPLERATE = 16000  # 采样率
CHANNELS = 1  # 单声道

# 主执行函数
def main(target_embedding):
    # 录制音频
    audio_data = denoise.denoise_audio(record.record_audio(5), SAMPLERATE, noise_start=0, noise_end=1)

    # 开始计时
    start_time = time.time()

    mixed_audio = preprocess_wav(audio_data, SAMPLERATE)
    target_segments = voiceprint.extract_target_speaker_segments(mixed_audio, target_embedding)
    
    if np.any(target_segments):
        print("Target speaker segments extracted.")
        print("Start recognizing...")
        result = recognise.recognize_audio(target_segments)
        print("Recognized text:", result)
        print("Recognizing finished.")
    else:
        print("No target speaker segments found.")
    print("Time elapsed:", time.time() - start_time)

# if __name__ == "__main__":
#     torchaudio.set_audio_backend("soundfile")
#     # 录制音频获取声纹特征
#     print("Model loaded.")
#     time.sleep(2)
#     target_audio = denoise.denoise_audio(record.record_audio(3), SAMPLERATE, noise_start=0, noise_end=1)
#     target_embedding = voiceprint.extract_voice_embedding(target_audio)
#     print("Voiceprint extracted.")
#     time.sleep(2)

#     while True:
#         main(target_embedding)
#         if input("Continue? (y/n)") != "y":
#             break
