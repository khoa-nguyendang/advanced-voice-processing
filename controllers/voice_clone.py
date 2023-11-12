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
from scipy.io.wavfile import write as write_wav
import os 
import uuid
 
device = "cuda:0" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(device)
rate = 44100
print('loaded voice_clone')

def voice_clone(input: str, speaker: str):
    file_output = os.path.abspath("./clone_output/voice_clone.wav")
    print(f'loaded voice_clone speaker path: {speaker} , file_output: {file_output}')
    # speech_output = tts.tts(text=input, language="en", speaker_wav=speaker)
    tts.tts_to_file(text=input, speaker_wav=speaker, language="en", file_path=file_output)
    return file_output


