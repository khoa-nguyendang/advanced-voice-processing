# advanced-voice-processing

## Preparation
1. Python3
2. Virtual env
3. CMake
4. NodeJS & npm 
5. GPU for inference



### Start server if CMake wasn't installed.

```
$ python3 -m venv env
$ . env/bin/activate
$ pip install -r requirements.txt
$ uvicorn main:app --reload
```

If CMake already install
```
$ make start
```

### Start web ui

To install NodeJS & NVM 
```
$ curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash 
$ nvm install --lts
```

Install packages

```
$ npm install -g @angular/cli
$ npm install --save-dev
```
