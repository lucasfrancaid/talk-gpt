# Back-end
Back-end built with Python, Pydub, gTTS, SpeechRecognition FastAPI and Pydantic.

## Install dependencies
If you don't already installed `poetry` in your machine, run:
```bash
pip install poetry
```

Initialize and install dependencies with `poetry`:
```bash
poetry shell
poetry install
```

## Settings
To communicate with `OpenAI` API is necessary to set up your `API_KEY`, so copy our `.env` example file:
```bash
cp .env.dev .env
```

Inside the `.env` change the variables with your keys.  

**NOTE**: If you don't already have the OPENAI keys, you can create here https://platform.openai.com/account/api-keys

## Server
To run the ASGI server:
```bash
python -m speak_gpt.server
```

Access: [http://localhost:3333/docs](http://localhost:3333/docs)

## CLI:
To start a chat via CLI:
```bash
python -m speak_gpt.cli
```

If you want to custom, read about more advanced configuration:
```bash
python -m speak_gpt.cli --help
```
