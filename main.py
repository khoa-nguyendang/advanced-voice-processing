import array
from pathlib import Path
from entities.request_model import RequestModel
from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import FileResponse
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
tmp_file_dir = "/tmp/example-files"
Path(tmp_file_dir).mkdir(parents=True, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/api/voice-translate")
async def voice_translate_api(request: Request, file: UploadFile = Form(...)):
    intput_file = os.path.join(tmp_file_dir, file.filename)
    with open(intput_file, 'wb') as disk_file:
        file_bytes = await file.read()
        disk_file.write(file_bytes)
    nda = load_audio(intput_file)

    textes = voice_translate(nda)
    data = text_to_speech(textes[0])
    print(textes)
    return FileResponse(data, media_type="audio/wav")

@app.post("/api/voice-recognize")
async def voice_recognize_api(request: Request, file: UploadFile = Form(...)):
    intput_file = os.path.join(tmp_file_dir, file.filename)
    with open(intput_file, 'wb') as disk_file:
        file_bytes = await file.read()
        disk_file.write(file_bytes)
    nda = load_audio(intput_file)
    output = voice_recognize(nda)
    return {"data": output}
    

@app.post("/api/voice-clone")
async def voice_clone_api(request: Request, file: UploadFile = Form(...), speaker: str = Form(...)):
    intput_file = os.path.join(tmp_file_dir, file.filename)
    with open(intput_file, 'wb') as disk_file:
        file_bytes = await file.read()
        disk_file.write(file_bytes)
    
    nda = load_audio(intput_file)
    input = voice_recognize(nda)
    print(input)
    data = voice_clone(input[0], speaker)
    return FileResponse(data, media_type="audio/wav")

@app.post("/api/text-to-speech")
def text_to_speech_api(model: RequestModel):
    print(model.text)
    data = text_to_speech(model.text)
    return FileResponse(data, media_type="audio/wav")


def load_audio(audio_path):
  """Load the audio file & convert to 16,000 sampling rate"""
  # load our wav file
  speech, sr = torchaudio.load(audio_path)
  resampler = torchaudio.transforms.Resample(sr, 16000)
  speech = resampler(speech)
  return speech.squeeze()