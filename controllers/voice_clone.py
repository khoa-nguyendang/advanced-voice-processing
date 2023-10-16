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

device = "cuda:0" if torch.cuda.is_available() else "cpu"
text = "Hello, my name is Manmay , how are you?"
PATH = os.path.abspath("models/text_2.pt")
tts = TTS("models/text_2.pt").to(device)
rate = 44100
print('loaded voice_clone')
# tts = TTS(PATH, gpu=True)


def voice_clone(input: str, speaker: str):
    # with random speaker
    # output_dict = model.synthesize(text, config, speaker_id="random", voice_dirs=None)

    # cloning a speaker.
    # It assumes that you have a speaker file in `bark_voices/speaker_n/speaker.wav` or `bark_voices/speaker_n/speaker.npz`
    # output_dict = model.synthesize(text, config, speaker_id="khoaspeech", voice_dirs="bark_voices/")
    
    if not (input and not input.isspace()):
        return None
    if not (speaker and not speaker.isspace()):
        speaker = "khoaspeech"
    tts.tts_to_file(text=input, file_path="voice_clone.wav", voice_dir="bark_voices/",speaker=speaker)
    return os.path.abspath("voice_clone.wav")
    # return open(PATH, 'rb') 
    
    # Audio(output_dict, rate=20000)
    # scaled = np.int16(output_dict / np.max(np.abs(output_dict)) * 32767)
    # write('test.wav', rate, scaled)