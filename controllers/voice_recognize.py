from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import torch
import os 


# load model and processor
device = "cuda:0" if torch.cuda.is_available() else "cpu"
PATH = os.path.abspath("models/tf_model.h5")
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2", local_files_only=False)
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2", local_files_only=False).to(device)
sampling_rate = 16000
print('loaded voice_recognize')
def voice_recognize(file_bytes) -> str:

    model.config.forced_decoder_ids = None

    # load dummy dataset and read audio files
    ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
    sample = ds[0]["audio"]
    print(f'sample type: {type(sample)}')
    print(sample)
    print(sample["sampling_rate"])
    
    input_features = processor(file_bytes, sampling_rate=sampling_rate, return_tensors="pt").input_features.to(device)

    # generate token ids
    predicted_ids = model.generate(input_features)
    # decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    print(transcription)
    return transcription