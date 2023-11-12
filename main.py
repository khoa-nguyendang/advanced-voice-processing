import array
from pathlib import Path
import threading
from entities.request_model import RequestModel
from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from controllers.text_to_speech import text_to_speech
from controllers.voice_clone import voice_clone
from controllers.voice_recognize import voice_recognize
from controllers.voice_translate import voice_translate
import torchaudio
import os
import numpy as np
import pickle
from scipy.io import wavfile


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tmp_file_dir = os.path.abspath("./voices_uploaded")
speaker_dir = os.path.abspath("./speaker_voices")
Path(tmp_file_dir).mkdir(parents=True, exist_ok=True)
Path(speaker_dir).mkdir(parents=True, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/api/voice-translate")
async def voice_translate_api(request: Request, file: UploadFile = Form(...)):
    print('voice_translate_api triggered')
    
    intput_file = os.path.join(tmp_file_dir, file.filename)
    with open(intput_file, 'wb') as disk_file:
        file_bytes = await file.read()
        disk_file.write(file_bytes)
        print(f'completed write intput_file {intput_file}' )
    nda = load_audio(intput_file)
    textes = voice_translate(nda)
    data = text_to_speech(textes[0])
    print(textes)
    return FileResponse(data, media_type="audio/wav")

@app.post("/api/voice-recognize")
async def voice_recognize_api(request: Request, file: UploadFile = Form(...)):
    print('voice_recognize_api triggered')
    
    intput_file = os.path.join(tmp_file_dir, file.filename)
    with open(intput_file, 'wb') as disk_file:
        file_bytes = await file.read()
        disk_file.write(file_bytes)
        print(f'completed write file {intput_file}' )
    nda = load_audio(intput_file)
    print(f'nda shape: {nda.shape}')
    output = voice_recognize(nda)
    return {"data": output}
    

@app.post("/api/voice-clone")
async def voice_clone_api(request: Request, file: UploadFile = Form(...), speaker: UploadFile = Form(...)):
    print('voice_clone_api triggered')
    #step 1. Store speaker to folder speaker_dir, target audio toi tmp_file_dir.
    intput_file = os.path.join(tmp_file_dir, file.filename)
    speaker_file = os.path.join(speaker_dir, speaker.filename)
    
    with open(intput_file, 'wb') as disk_file:
        file_bytes = await file.read()
        disk_file.write(file_bytes)
        print(f'completed write intput_file {intput_file}' )
        
    with open(speaker_file, 'wb') as speaker_disk_file:
        speaker_file_bytes = await speaker.read()
        speaker_disk_file.write(speaker_file_bytes)
        print(f'completed write speaker_file {speaker_file}' )
        
    nda = load_audio(intput_file)
    input = voice_recognize(nda)
    print(f'text from audio : {input}')
    data = voice_clone(input[0], speaker_file)
    return FileResponse(data, media_type="audio/wav")

@app.post("/api/text-to-speech")
def text_to_speech_api(model: RequestModel):
    print('text_to_speech_api triggered')
    print(model.text)
    data = text_to_speech(model.text)
    return FileResponse(data, media_type="audio/wav")


def load_audio(audio_path):
  """Load the audio file & convert to 16,000 sampling rate"""
  print(f'loading audio: {audio_path}')
  # load our wav file
  speech, sample_rate = torchaudio.load(audio_path)
  resampler = torchaudio.transforms.Resample(sample_rate, 16000)
  speech = resampler(speech)
  print(f'audio loaded {speech.shape}')
  result = speech.squeeze()
  print(f'audio nd result {result.shape}')
  if result.size(dim=1) > 1:
    print('detected multiple channel audio file')
    speech2, sample_rate = torchaudio.load(audio_path)
    speech2 = resampler(speech2[0,:].view(1,-1))
    result = speech2.squeeze()
    print(f'new audio nd result {result.shape}')
  return result

async def save_audio(file: UploadFile, intput_file: str):
    with open(intput_file, 'wb') as disk_file:
        file_bytes = await file.read()
        disk_file.write(file_bytes)
        