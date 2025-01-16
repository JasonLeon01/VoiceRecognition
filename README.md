# VoiceRecognition
## Installation
First, install Python 3.8.0 or higher version. Clone this repository and install dependencies and models.

[Here](https://alphacephei.com/vosk/models) is the download address of vosk model.

```bash
pip install -r requirements.txt
# If you have GPU
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# Otherwise
pip3 install torch torchvision torchaudio
```
## Used Repos
### noisereduce
This repository is used to denoise. It works by computing a spectrogram of a signal (and optionally a noise signal) and estimating a noise threshold (or gate) for each frequency band of that signal/noise.

**It does not rely on machine learning.**

https://github.com/timsainb/noisereduce

### Reseemblyzer
This repository is used to extract voiceprint features and compare the similarity of the voice with the recorded voiceprint.

https://github.com/resemble-ai/Resemblyzer

### vosk
This repository is used to recognise voices. Its official website provides a large number of models. 

https://alphacephei.com/vosk/models

Here is the python api address: https://github.com/alphacep/vosk-api/tree/master/python

However, you can also train your own model by this. 

https://github.com/alphacep/vosk-api/tree/master/training
