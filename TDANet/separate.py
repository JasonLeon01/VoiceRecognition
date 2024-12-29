import os
import torch
import look2hear.models
import torchaudio

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

mix, sr = torchaudio.load("outfile.wav")
transform = torchaudio.transforms.Resample(sr, 16_000)
mix = transform(mix)
mix = mix.view(1, 1, -1)
model = look2hear.models.BaseModel.from_pretrain("./local_models/TDANetBest-4ms-LRS2/pytorch_model.bin").to(device)
est_sources = model(mix.to(device))
torchaudio.save("audio_1_sep.wav", est_sources[:, 0, :].detach().cpu(), 16_000)
torchaudio.save("audio_2_sep.wav", est_sources[:, 1, :].detach().cpu(), 16_000)