from TTS.api import TTS
from transformers import AutoProcessor, BarkModel, pipeline
import torch
import os 
from scipy.io.wavfile import write as write_wav


# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# print(device)
# print(f'device count{torch.cuda.device_count()}')
# # PATH = os.path.abspath("models/text_2.pt")
# # print(PATH)
# processor = AutoProcessor.from_pretrained("suno/bark")
# model = BarkModel.from_pretrained("suno/bark").to(device)
# # model =  model.to_bettertransformer()

device = "cuda:0" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(device)
rate = 44100

print('loaded text_to_speech')
def text_to_speech(input: str):
    # # synthesiser = pipeline("text-to-speech", "suno/bark")
    # inputs = processor(input)

    # # generate speech
    # speech_output = model.generate(**inputs.to(device))
    # sampling_rate = model.generation_config.sample_rate
    # write_wav("text_to_speech_output.wav", rate=sampling_rate, data=speech_output[0].cpu().numpy())
    # # save audio to disk, but first take the sample rate from the model config
    # # write_wav("text_to_speech_output.wav", rate=speech["sampling_rate"], data=speech["audio"])
    # return os.path.abspath("text_to_speech_output.wav")
    
    file_output = os.path.abspath("./clone_output/text_to_speech.wav")
    speaker = os.path.abspath('./speaker_voices/speaker_n/khoaspeech.wav')
    print(f'loaded text_to_speech speaker path: {speaker} , file_output: {file_output}')
    # speech_output = tts.tts(text=input, language="en", speaker_wav=speaker)
    tts.tts_to_file(text=input, speaker_wav=speaker, language="en", file_path=file_output)
    return file_output
