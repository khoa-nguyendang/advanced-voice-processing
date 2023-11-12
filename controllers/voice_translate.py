from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import Audio, load_dataset
import torch
import os 


# load model and processor
device = "cuda:0" if torch.cuda.is_available() else "cpu"
PATH = os.path.abspath("models/tf_model.h5")
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2", local_files_only=False)
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2", local_files_only=False).to(device)
sampling_rate = 16000

print('loaded voice_translate')
def voice_translate(ndarray):
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="vietnamese", task="translate")
    # load streaming dataset and read first audio sample
    # ds = load_dataset("common_voice", "vn", split="test", streaming=True)
    # ds = ds.cast_column("audio", Audio(sampling_rate=16_000))
    # input_speech = next(iter(ds))["audio"]
    
    input_features = processor(ndarray, sampling_rate=sampling_rate, return_tensors="pt").input_features.to(device)

    # generate token ids
    predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
    
    # decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    print(transcription)
    return transcription