from Resemblyzer.resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

encoder = VoiceEncoder()

# 声纹特征提取函数
def extract_voice_embedding(audio_data, sample_rate=16000):
    print("Extracting voice embedding...")
    wav = preprocess_wav(audio_data, sample_rate)  # 预处理音频数据
    embedding = encoder.embed_utterance(wav)  # 提取声纹特征
    print("Voice embedding extracted.")
    return embedding

# 音频分段
def split_audio(audio_data, segment_duration, SAMPLERATE=16000):
    segment_length = int(SAMPLERATE * segment_duration)
    return [audio_data[i:i + segment_length] for i in range(0, len(audio_data), segment_length)]

# 从音频中提取目标说话人的音频段
def extract_target_speaker_segments(audio_data, target_embedding, segment_duration=0.5, SAMPLERATE=16000):
    audio_segments = split_audio(audio_data, segment_duration)
    segment_length = int(SAMPLERATE * segment_duration)
    target_segments = np.zeros_like(audio_data)
    
    for i, segment in enumerate(audio_segments):
        # 提取当前分段的声纹特征
        segment_embedding = encoder.embed_utterance(segment)
        similarity = np.dot(segment_embedding, target_embedding) / (np.linalg.norm(segment_embedding) * np.linalg.norm(target_embedding))  # 计算相似度

        # 如果相似度高于阈值，认为是目标说话人的声音
        print(f"Segment {i + 1} similarity: {similarity}")
        if similarity > 0.55:  # 阈值可以根据实际情况调整
            start = i * segment_length
            end = start + len(segment)  # 使用实际长度，以处理不足一个分段的部分
            target_segments[start:end] = segment  # 提取目标说话人的声音

    return target_segments
