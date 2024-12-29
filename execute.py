import os
import sys
import sounddevice as sd
import numpy as np
import torch
import torchaudio
from io import BytesIO
from vosk import Model, KaldiRecognizer
import wave
import TDANet.look2hear.models
import threading

# 设备设置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 录音参数
SAMPLERATE = 16000  # 采样率
CHANNELS = 1  # 单声道
DURATION = 5  # 录制时长，单位为秒

# 录制音频的函数
def record_audio():
    print("Start recording...")
    audio_data = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=CHANNELS, dtype='float32')
    sd.wait()  # 等待录音完成
    print("Recording finished.")
    return audio_data

# 分离音频的函数
def separate_audio(mix_audio):
    print("Start separating...")
    mix_audio = torch.from_numpy(mix_audio).view(1, 1, -1)  # 转换为 PyTorch tensor
    model = TDANet.look2hear.models.BaseModel.from_pretrain("./TDANet/local_models/TDANetBest-4ms-LRS2/pytorch_model.bin").to(device)
    est_sources = model(mix_audio.to(device))  # 执行分离
    print("Separation finished.")
    return est_sources

# 语音识别函数
def recognize_audio(audio_data, sample_rate, model_path, result_container):
    # 加载 Vosk 模型
    print("Start recognizing...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)

    # 将 bytes 对象转换为 NumPy 数组
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # 分块识别音频
    recognizer.AcceptWaveform(audio_array.tobytes())
    result = recognizer.FinalResult()

    # 将结果存入容器
    result_container.append(result)
    print("Recognizing finished.")

# 主执行函数
def main():
    # 录制音频
    audio_data = record_audio()

    # 分离音频
    est_sources = separate_audio(audio_data)

    # 将分离的音频保存到内存（BytesIO对象）
    buffer_1 = BytesIO()
    buffer_2 = BytesIO()

    # 保存音频到内存，先转换为 PCM_16 格式
    torchaudio.save(buffer_1, (est_sources[:, 0, :].detach().cpu() * 32767).to(torch.int16), SAMPLERATE, format="wav")
    torchaudio.save(buffer_2, (est_sources[:, 1, :].detach().cpu() * 32767).to(torch.int16), SAMPLERATE, format="wav")

    # 重设文件指针到文件开头
    buffer_1.seek(0)
    buffer_2.seek(0)

    # 加载音频数据
    with wave.open(buffer_1, 'rb') as wf:
        audio_data_1 = wf.readframes(wf.getnframes())
    with wave.open(buffer_2, 'rb') as wf:
        audio_data_2 = wf.readframes(wf.getnframes())
        
    # 创建结果容器
    result_1 = []
    result_2 = []

    # 识别音频
    model_path = "./vosk-model-small-cn-0.22"
    thread_1 = threading.Thread(target=recognize_audio, args=(audio_data_1, SAMPLERATE, model_path, result_1))
    thread_2 = threading.Thread(target=recognize_audio, args=(audio_data_2, SAMPLERATE, model_path, result_2))
    thread_1.start()
    thread_2.start()
    
    # 等待线程完成
    thread_1.join()
    thread_2.join()

    # 输出识别结果
    print("Voice 1:", result_1[0])
    print("Voice 2:", result_2[0])

if __name__ == "__main__":
    main()
