import json
import sounddevice as sd
import numpy as np
import torch
import torchaudio
from vosk import Model, KaldiRecognizer
import TDANet.look2hear.models
import time
from concurrent.futures import ThreadPoolExecutor

# 设备设置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
separation_model = TDANet.look2hear.models.BaseModel.from_pretrain(
    "./TDANet/local_models/TDANetBest-4ms-LRS2/pytorch_model.bin"
).to(device)
separation_model.eval()
recognition_model_path = "./vosk-model-cn-0.22"
recognition_model = Model(recognition_model_path)

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
    with torch.no_grad():  # 禁用梯度计算
        est_sources = separation_model(mix_audio.to(device))
    print("Separation finished.")
    return est_sources

# 语音识别函数
def recognize_audio(audio_data, sample_rate, result_container):
    print("Start recognizing...")
    recognizer = KaldiRecognizer(recognition_model, sample_rate)
    recognizer.AcceptWaveform(audio_data.tobytes())
    result = recognizer.FinalResult()
    result_dict = json.loads(result)
    text = result_dict.get("text", "")
    result_container.append(text)
    print("Recognizing finished.")

# 并行处理识别任务
def parallel_recognize(audio_data_1, audio_data_2, sample_rate, result_1, result_2):
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务，并将结果存入各自的容器
        executor.submit(recognize_audio, audio_data_1, sample_rate, result_1)
        executor.submit(recognize_audio, audio_data_2, sample_rate, result_2)

# 主执行函数
def main():
    torchaudio.set_audio_backend("soundfile")
    # 录制音频
    audio_data = record_audio()

    # 开始计时
    start_time = time.time()

    # 分离音频
    est_sources = separate_audio(audio_data)

    # 转为 NumPy 数组
    audio_data_1 = (est_sources[:, 0, :].detach().cpu() * 32767).numpy().astype(np.int16)
    audio_data_2 = (est_sources[:, 1, :].detach().cpu() * 32767).numpy().astype(np.int16)

    # 并行识别
    result_1, result_2 = [], []
    parallel_recognize(audio_data_1, audio_data_2, SAMPLERATE, result_1, result_2)

    # 输出结果
    print("Voice 1:", result_1[0])
    print("Voice 2:", result_2[0])
    print("Time elapsed:", time.time() - start_time)

if __name__ == "__main__":
    while True:
        main()
        if input("Continue? (y/n)") != "y":
            break
