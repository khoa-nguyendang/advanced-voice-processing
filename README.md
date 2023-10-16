# advanced-voice-processing

## Preparation

step 0. add submodules if not exists
```
git submodule add https://github.com/coqui-ai/TTS.git externals/tts/
```

step 1. Pull submodule

```
git submodule update --init
git submodule update --recursive --remote
git pull --recurse-submodules
```

step 2. Build docker image tts
```
cd externals/tts/
make system-deps  # only on Linux systems.
make install
```

step 3. Download speaker you want to clone or make it yourself to  `bark_voices/speaker_n/` directory

```
https://huggingface.co/datasets/hf-internal-testing/librispeech_asr_dummy
```


### Run by docker options

start docker
```
docker run --rm -it -p 5002:5002 --gpus all --entrypoint /bin/bash ghcr.io/coqui-ai/tts
python3 TTS/server/server.py --list_models #To get the list of available models
python3 TTS/server/server.py --model_name tts_models/en/vctk/vits --use_cuda true

```



### Run by code options
step 0. add submodules if not exists
```
git submodule add https://github.com/coqui-ai/TTS.git externals/tts/
```

step 1. Pull submodule

```
git submodule update --init
git submodule update --recursive --remote
git pull --recurse-submodules
```

step 2. Active virtual 