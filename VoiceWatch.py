import queue
import json
import threading
import time
import numpy as np
import sounddevice as sd
import noisereduce as nr
from vosk import Model, KaldiRecognizer
import webrtcvad
from Resemblyzer.resemblyzer import VoiceEncoder, preprocess_wav

class Listener:
    def __init__(self, wake_word, GUI_update_callback):
        self.wake_word = wake_word
        self.GUI_update_callback = GUI_update_callback
        self.is_listening = False

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

        self.frame_duration_ms = 30  # 每帧持续30毫秒
        self.frame_length = int(self.SAMPLERATE * self.frame_duration_ms / 1000)  # 每帧的采样点数
        self.buffer = []  # 用来存储累积的音频数据，但只处理每帧的数据
        self.vad = webrtcvad.Vad(3)
    
    def denoise_audio(self, audio_data):
        print("Denoising audio...")
        noise = audio_data[: min(len(audio_data), int(0.5 * self.SAMPLERATE))]
        reduced_noise = nr.reduce_noise(y=audio_data, sr=self.SAMPLERATE, y_noise=noise)
        print("Audio denoised.")
        return reduced_noise
    
    def detect_speech(self):
        if len(self.buffer) < self.frame_length:  # 如果积累的数据不够一帧的大小
            return False, None
        
        # 获取一帧数据（每帧30ms的数据）
        frame = self.buffer[:self.frame_length]
        self.buffer = self.buffer[self.frame_length:]  # 移除已处理的帧数据

        # 检测这帧数据是否含有语音
        frame_int16 = np.int16(np.array(frame) * 32767).flatten()
        is_speech = self.vad.is_speech(frame_int16.tobytes(), self.SAMPLERATE)
        return is_speech, frame

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        # 将音频数据转换为16-bit PCM数据并累积
        # indata_int16 = np.int16(indata * 32767)  # float32 转 int16
        self.buffer.extend(indata.flatten())  # 将数据追加到 buffer

    def listen(self):
        with sd.InputStream(samplerate=self.SAMPLERATE, channels=self.CHANNELS, callback=self.callback):
            print("Start watching...")
            audio_buffer = np.array([], dtype=np.float32)
            while self.is_listening:
                try:
                    if len(self.buffer) >= self.frame_length:
                        is_speech, frame = self.detect_speech()
                        if is_speech:
                            audio_buffer = np.concatenate((audio_buffer, frame))
                            print("Speech detected.")
                            self.speech_detected = True
                            if self.last_detected_time is None:
                                self.last_detected_time = time.time()
                            if time.time() - self.last_detected_time > 10:
                                self.speech_detected = False
                                self.last_detected_time = None
                        else:
                            if self.speech_detected:
                                saved_audio_buffer = None
                                if self.target_embedding is None:
                                    if time.time() - self.last_detected_time > 1:
                                        self.speech_detected = False
                                        self.last_detected_time = None
                                        saved_audio_buffer = audio_buffer.flatten()
                                        audio_buffer = np.array([], dtype=np.float32)
                                        clean_audio = self.denoise_audio(saved_audio_buffer)
                                        text = self.recognize_audio(clean_audio)

                                        print(f"Recognized text: {text}")
                                        if self.wake_word in text:
                                            print("Wake word detected.")
                                            self.target_embedding = self.voiceprint.extract_voice_embedding(clean_audio)
                                            print("Target speaker set. Please start speaking.")
                                else:
                                    if time.time() - self.last_detected_time > 6:
                                        self.speech_detected = False
                                        self.last_detected_time = None
                                        audio_buffer = np.array([], dtype=np.float32)
                                        self.target_embedding = None
                                        print("Target speaker cleared.")
                                        continue
                                    if time.time() - self.last_detected_time > 1:
                                        self.speech_detected = False
                                        saved_audio_buffer = audio_buffer.flatten()
                                        audio_buffer = np.array([], dtype=np.float32)
                                        clean_audio = self.denoise_audio(saved_audio_buffer)

                                        target_audio = self.voiceprint.extract_target_speaker_segments(clean_audio, self.target_embedding, 0.5)

                                        if np.any(target_audio):
                                            self.last_detected_time = None
                                            text = self.recognize_audio(target_audio)
                                            print(f"Recognized target text: {text}")
                                            self.stop_listening()
                                            self.GUI_update_callback(text)

                            else:
                                audio_buffer = np.array([], dtype=np.float32)

                except Exception as e:
                    print(e)

    def recognize_audio(self, audio_data):
        print(audio_data)
        self.recognizer.Reset()
        # audio_int16 = audio_data.astype(np.int16)
        audio_int16 = np.int16(audio_data * 32767).flatten()
        self.recognizer.AcceptWaveform(audio_int16.tobytes())
        result = self.recognizer.FinalResult()
        result_dict = json.loads(result)
        return result_dict.get("text", "").replace(" ", "")

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
