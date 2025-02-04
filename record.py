import sounddevice as sd

# 录制音频的函数
def record_audio(DURATION, SAMPLERATE=16000, CHANNELS=1):
    print("Start {} seconds recording...".format(DURATION))
    audio_data = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=CHANNELS, dtype='float32')
    sd.wait()  # 等待录音完成
    print("Recording finished.")
    return audio_data.flatten()
