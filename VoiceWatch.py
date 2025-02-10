import queue
import json
import threading
import time
import numpy as np
import sounddevice as sd
import noisereduce as nr
from vosk import Model, KaldiRecognizer
from Resemblyzer.resemblyzer import VoiceEncoder, preprocess_wav

class Listener:
    def __init__(self, wake_word, GUI_update_callback):
        self.wake_word = wake_word
        self.GUI_update_callback = GUI_update_callback
        self.is_listening = False

        self.audio_queue = queue.Queue()
        # 录音参数
        self.SAMPLERATE = 16000  # 采样率
        self.CHANNELS = 1  # 单声道

        recognition_model_path = "./vosk-model-cn-0.22"
        self.recognition_model = Model(recognition_model_path)
        self.recognizer = KaldiRecognizer(self.recognition_model, self.SAMPLERATE)

        self.target_embedding = None
        self.last_detected_time = None
        self.speech_detected = False
        self.voiceprint = Voiceprint()
    
    def denoise_audio(self, audio_data):
        print("Denoising audio...")
        noise = audio_data[: min(len(audio_data), int(0.5 * self.SAMPLERATE))]
        reduced_noise = nr.reduce_noise(y=audio_data, sr=self.SAMPLERATE, y_noise=noise)
        print("Audio denoised.")
        return reduced_noise
    
    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata.copy())

    def listen(self):
        with sd.InputStream(samplerate=self.SAMPLERATE, channels=self.CHANNELS, callback=self.callback):
            print("Start watching...")
            while self.is_listening:
                try:
                    # 从队列中获取音频数据
                    data = self.audio_queue.get()
                    audio_data = data.flatten().astype(np.float32)
                    
                    # 降噪处理
                    clean_audio = self.denoise_audio(audio_data)
                    
                    # 语音识别
                    text = self.recognize_audio(clean_audio)
                    if text:
                        print("Word viewing", text)

                        # 检测是否包含唤醒词
                        if self.wake_word in text:
                            self.target_embedding = self.voiceprint.extract_voice_embedding(clean_audio)
                            self.last_detected_time = time.time()
                            self.speech_detected = True
                            self.GUI_update_callback()  # 调用唤醒后执行的函数
                            continue

                    if self.target_embedding is not None:
                        target_audio = self.voiceprint.extract_target_speaker_segments(clean_audio, self.target_embedding, 0.55)
                        if np.any(target_audio):
                            print("Target speaker segments extracted.")
                            self.last_detected_time = time.time()
                            self.speech_detected = True
                        elif time.time() - self.last_detected_time > 1:
                            final_text = self.recognize_audio(clean_audio)
                            if final_text:
                                print("Final text:", final_text)
                                self.GUI_update_callback(final_text)
                            self.speech_detected = False

                        if time.time() - self.last_detected_time > 10:
                            self.target_embedding = None
                            self.last_detected_time = None
                            self.speech_detected = False

                except Exception as e:
                    print(e)

    def recognize_audio(self, audio_data):
        self.recognizer.Reset()
        self.recognizer.AcceptWaveform((audio_data * 32767).astype(np.int16).tobytes())
        result = self.recognizer.FinalResult()
        try:
            result_dict = json.loads(result)
            return result_dict.get("text", "").strip()
        except json.JSONDecodeError:
            return ""

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            listen_thread = threading.Thread(target=self.listen)
            listen_thread.start()

    def stop_listening(self):
        self.is_listening = False
        sd.stop()
        print("Stop watching...")

class Voiceprint:
    def __init__(self):
        self.encoder = VoiceEncoder()
        self.SAMPLERATE = 16000

    def extract_voice_embedding(self, audio_data):
        print("Extracting voice embedding...")
        wav = preprocess_wav(audio_data, self.SAMPLERATE)  # 预处理音频数据
        embedding = self.encoder.embed_utterance(wav)  # 提取声纹特征
        print("Voice embedding extracted.")
        return embedding

    def split_audio(self, audio_data, segment_duration):
        segment_length = int(self.SAMPLERATE * segment_duration)
        return [audio_data[i:i + segment_length] for i in range(0, len(audio_data), segment_length)]
    
    def extract_target_speaker_segments(self, audio_data, target_embedding, in_similarity, segment_duration=0.5):
        audio_segments = self.split_audio(audio_data, segment_duration)
        segment_length = int(self.SAMPLERATE * segment_duration)
        target_segments = np.zeros_like(audio_data)
        
        for i, segment in enumerate(audio_segments):
            # 提取当前分段的声纹特征
            segment_embedding = self.encoder.embed_utterance(segment)

            if np.linalg.norm(segment_embedding) == 0 or np.linalg.norm(target_embedding) == 0:
                continue

            similarity = np.dot(segment_embedding, target_embedding) / (np.linalg.norm(segment_embedding) * np.linalg.norm(target_embedding))  # 计算相似度

            # 如果相似度高于阈值，认为是目标说话人的声音
            print(f"Segment {i + 1} similarity: {similarity}")
            if similarity > in_similarity:  # 阈值可以根据实际情况调整
                start = i * segment_length
                end = start + len(segment)  # 使用实际长度，以处理不足一个分段的部分
                target_segments[start:end] = segment  # 提取目标说话人的声音

        return target_segments
