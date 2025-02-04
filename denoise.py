import noisereduce as nr

# 降噪函数
def denoise_audio(audio_data, sample_rate, noise_start=0, noise_end=1):
    print("Denoising audio...")
    noise = audio_data[int(noise_start * sample_rate):int(noise_end * sample_rate)]
    reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate, y_noise=noise)
    print("Audio denoised.")
    return reduced_noise
