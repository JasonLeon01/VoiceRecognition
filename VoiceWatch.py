import io
import threading
import time
import numpy as np
import sounddevice as sd
import torch
import noisereduce as nr
import whisper
import webrtcvad
from Resemblyzer.resemblyzer import VoiceEncoder, preprocess_wav
import speech_recognition as sr
import soundfile as sf

class Listener:
    def __init__(self, wake_word, GUI_update_callback):
        self.wake_word = wake_word
        self.device = f'cuda' if torch.cuda.is_available() else 'cpu'
        self.GUI_update_callback = GUI_update_callback
        self.is_listening = False

        self.language_prompt = {
            "zh": "以下是普通话内容，但是如果没有识别出任何内容，则不要输出。",
            "en": "The following is English content, but if nothing is recognized, do not output."
        }

        # 录音参数
        self.SAMPLERATE = 16000  # 采样率
        self.CHANNELS = 1  # 单声道

        self.whisper_model = whisper.load_model("turbo")
        self.recognizer = sr.Recognizer()

        self.target_embedding = None
        self.last_detected_time = None
        self.speech_detected = False
        self.voiceprint = Voiceprint()
        self.detected_audio = None

        self.frame_duration_ms = 30  # 每帧持续30毫秒
        self.frame_length = int(self.SAMPLERATE * self.frame_duration_ms / 1000)  # 每帧的采样点数
        self.buffer = []  # 用来存储累积的音频数据，但只处理每帧的数据
        self.vad = webrtcvad.Vad(3)
    
    def denoise_audio(self, audio_data):
        noise = audio_data[: min(len(audio_data), int(0.5 * self.SAMPLERATE))]
        reduced_noise = nr.reduce_noise(y=audio_data, sr=self.SAMPLERATE, y_noise=noise)
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
    
    def is_speech(self, audio_array):
        if audio_array.ndim > 1:
            audio_array = audio_array.mean(axis=1)

        audio_array = (audio_array * 32767).astype(np.int16)
        return self.vad.is_speech(audio_array.tobytes(), self.SAMPLERATE)

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        # 将音频数据转换为16-bit PCM数据并累积

        self.buffer.extend(indata.flatten())  # 将数据追加到 buffer

    def listen(self):
        while self.is_listening:
            with sr.Microphone() as source:
                print("Start watching...")
                audio = self.recognizer.listen(source)

            print("Watching ended.")
            wav_bytes = audio.get_wav_data(convert_rate=self.SAMPLERATE)
            wav_stream = io.BytesIO(wav_bytes)
            audio_array, sampling_rate = sf.read(wav_stream)
            audio_array = audio_array.astype(np.float32)

            frame_length = int(self.SAMPLERATE * self.frame_duration_ms / 1000)
            num_frames = len(audio_array) // frame_length
            remainder = len(audio_array) % frame_length

            if remainder != 0:
                padding_length = frame_length - remainder
                audio_array = np.pad(audio_array, (0, padding_length), mode='constant')

            audio_array_speech = (audio_array * 32767).astype(np.int16)

            speech_count = 0
            for i in range(num_frames):
                frame = audio_array_speech[i * frame_length:(i + 1) * frame_length]
                if self.is_speech(frame):
                    speech_count += 1

            if speech_count > num_frames // 2:
                print("Speech detected.")
                text, language = self.language_detect(audio_array)
                self.stop_listening()
                self.GUI_update_callback(text)
            else:
                print("It's not person speaking.")
                continue

    def language_detect(self, audio_data):
        if self.device == 'cuda':
            fp16 = True
        else:
            fp16 = False
        
        audio_pot = whisper.pad_or_trim(audio_data)
        mel = whisper.log_mel_spectrogram(audio_pot, n_mels=self.whisper_model.dims.n_mels).to(self.whisper_model.device)
        _, probs = self.whisper_model.detect_language(mel)

        language = max(probs, key=probs.get)
        print(f"Detected language: {language}")

        if language in self.language_prompt:
            initial_prompt = self.language_prompt[language]
        else:
            initial_prompt = "Show the content in the detected language."

        result = self.whisper_model.transcribe(
            audio_data,
            language=language,
            fp16=fp16,
            temperature=0.2,
            initial_prompt=initial_prompt
        )

        print(f"Transcription result: {result['text']}")
        return result["text"], language

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