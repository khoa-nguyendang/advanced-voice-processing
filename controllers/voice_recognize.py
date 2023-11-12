from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import torch
import os 


# load model and processor
device = "cuda:0" if torch.cuda.is_available() else "cpu"
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2", local_files_only=False)
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2", local_files_only=False).to(device)
sampling_rate = 16000
model.config.forced_decoder_ids = None

print('loaded voice_recognize')
def voice_recognize(ndarray) -> str:
    print(f'ndarray shape: {ndarray.shape}')
    input_features = processor(audio=ndarray, sampling_rate=sampling_rate, return_tensors="pt").input_features.to(device)
    # generate token ids
    predicted_ids = model.generate(input_features)
    # decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    print(transcription)
    return transcription