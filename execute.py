import json
import os
import sys
import sounddevice as sd
import numpy as np
import torch
import torchaudio
sys.path.append(os.path.join(os.getcwd(), 'Resemblyzer'))
import noisereduce as nr
from vosk import Model, KaldiRecognizer
from Resemblyzer.resemblyzer import VoiceEncoder, preprocess_wav
# from pathlib import Path
import time
# from concurrent.futures import ThreadPoolExecutor

print("Prepare model.")
# 设备设置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 录音参数
SAMPLERATE = 16000  # 采样率
CHANNELS = 1  # 单声道

recognition_model_path = "./vosk-model-cn-0.22"
recognition_model = Model(recognition_model_path)
recognizer = KaldiRecognizer(recognition_model, SAMPLERATE)
encoder = VoiceEncoder()

# 录制音频的函数
def record_audio(DURATION):
    print("Start {} seconds recording...".format(DURATION))
    audio_data = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=CHANNELS, dtype='float32')
    sd.wait()  # 等待录音完成
    print("Recording finished.")
    return audio_data.flatten()

# 降噪函数
def denoise_audio(audio_data, sample_rate, noise_start=0, noise_end=1):
    print("Denoising audio...")
    noise = audio_data[int(noise_start * sample_rate):int(noise_end * sample_rate)]
    reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate, y_noise=noise)
    print("Audio denoised.")
    return reduced_noise

# 声纹特征提取函数
def extract_voice_embedding(audio_data, sample_rate=SAMPLERATE):
    print("Extracting voice embedding...")
    wav = preprocess_wav(audio_data, sample_rate)  # 预处理音频数据
    embedding = encoder.embed_utterance(wav)  # 提取声纹特征
    print("Voice embedding extracted.")
    return embedding

# 音频分段
def split_audio(audio_data, segment_duration):
    segment_length = int(SAMPLERATE * segment_duration)
    return [audio_data[i:i + segment_length] for i in range(0, len(audio_data), segment_length)]

# 从音频中提取目标说话人的音频段
def extract_target_speaker_segments(audio_data, target_embedding, segment_duration=0.5):
    audio_segments = split_audio(audio_data, segment_duration)
    segment_length = int(SAMPLERATE * segment_duration)
    target_segments = np.zeros_like(audio_data)
    for i, segment in enumerate(audio_segments):
        if len(segment) < segment_length:
            continue  # 忽略最后不足一个分段的部分

        # 提取当前分段的声纹特征
        segment_embedding = encoder.embed_utterance(segment)
        similarity = np.dot(segment_embedding, target_embedding) / (np.linalg.norm(segment_embedding) * np.linalg.norm(target_embedding))  # 计算相似度

        # 如果相似度高于阈值，认为是目标说话人的声音
        print(f"Segment {i + 1} similarity: {similarity}")
        if similarity > 0.65:  # 阈值可以根据实际情况调整
            start = i * segment_length
            end = start + segment_length
            target_segments[start:end] = segment  # 提取目标说话人的声音
    return target_segments

# 语音识别函数
def recognize_audio(audio_data):
    recognizer.Reset()
    recognizer.AcceptWaveform((audio_data * 32767).astype(np.int16).tobytes())
    result = recognizer.FinalResult()
    result_dict = json.loads(result)
    return result_dict.get("text", "")

# 主执行函数
def main(target_embedding):
    # 录制音频
    audio_data = denoise_audio(record_audio(5), SAMPLERATE, noise_start=0, noise_end=1)

    # 开始计时
    start_time = time.time()

    mixed_audio = preprocess_wav(audio_data, SAMPLERATE)
    target_segments = extract_target_speaker_segments(mixed_audio, target_embedding)
    
    if np.any(target_segments):
        print("Target speaker segments extracted.")
        print("Start recognizing...")
        result = recognize_audio(target_segments)
        print("Recognized text:", result)
        print("Recognizing finished.")
    else:
        print("No target speaker segments found.")
    print("Time elapsed:", time.time() - start_time)

if __name__ == "__main__":
    torchaudio.set_audio_backend("soundfile")
    # 录制音频获取声纹特征
    target_audio = denoise_audio(record_audio(3), SAMPLERATE, noise_start=0, noise_end=1)
    target_embedding = extract_voice_embedding(target_audio)
    print("Voiceprint extracted.")
    time.sleep(2)

    while True:
        main(target_embedding)
        if input("Continue? (y/n)") != "y":
            break
