# from transformers import pipeline
# import scipy

# from transformers import AutoProcessor, AutoModel

# processor = AutoProcessor.from_pretrained("suno/bark")
# model = AutoModel.from_pretrained("suno/bark")

# inputs = processor(
#     text=["Hello, my name is Suno. And, uh — and I like pizza. [laughs] But I also have other interests such as playing tic tac toe."],
#     return_tensors="pt",
# )

# speech_values = model.generate(**inputs, do_sample=True)


from TTS.api import TTS
import torch
import os 
# from IPython.display import Audio
# from scipy.io.wavfile import write
# import numpy as np

import os 
import uuid
 
device = "cuda:0" if torch.cuda.is_available() else "cpu"
text = "Hello, my name is Manmay , how are you?"
PATH = os.path.abspath("../models/text_2.pt")
tts = TTS(PATH).to(device)
rate = 44100
print('loaded voice_clone')

def voice_clone(input: str, speaker: str):
    print(f'loaded voice_clone, model path: {PATH} , speaker path: {speaker}')
    tts.tts_to_file(text=input, file_path="../clone_ouput/voice_clone.wav",  language="en", speaker_wav=speaker)
    return os.path.abspath("voice_clone.wav")
