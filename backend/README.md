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
python -m talk_gpt.server
# or: talk_gpt --cmd api
```

To run by specifying your environment variables file:
```bash
python -m talk_gpt.server --env-file <ENV_FILE>
# or: talk_gpt --cmd api --env-file <ENV_FILE>
```

Access: [http://localhost:8000/docs](http://localhost:8000/docs)

## CLI
To start a chat via CLI:
```bash
talk_gpt --cmd cli
```

To start via CLI listening responses in audio:
```bash
talk_gpt --cmd cli.audio
```

Give a name to your chat and reuse that easy:
```bash
talk_gpt --cmd cli --chat-id <CHAT_NAME>
# Then you can always run this command and get your historic
```

To start with your keys without any configuration:
```bash
talk_gpt --openai-key <YOUR_KEY> --openai-org <YOUR_ORG>
```

For more custom settings:
```bash
talk_gpt --help
```
