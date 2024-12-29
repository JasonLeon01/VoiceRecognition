# VoiceRecognition
## Installation
First, install Python 3.8.0 or higher version. Clone this repository and install dependencies and models.

[Here](https://alphacephei.com/vosk/models) is the download address of vosk model.

[Here](https://huggingface.co/JusperLee/TDANetBest-4ms-LRS2) is the download address of TDANet model.

```bash
pip install -r requirements.txt
# If you have GPU
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# Otherwise
pip3 install torch torchvision torchaudio
```

