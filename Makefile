.PHONY: pepare start stop download

download:
	wget -P ./models https://huggingface.co/suno/bark/resolve/main/text_2.pt

prepare:
	python3 -m venv env & . ./env/bin/activate & pip install -r requirements.txt

start:
	uvicorn main:app --reload
	

