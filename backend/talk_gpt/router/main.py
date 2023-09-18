from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from talk_gpt.audio.speech import VOICE_FROM_FILE, speech_to_text, text_to_speech
from talk_gpt.gpt.chat import TalkGPT
from talk_gpt.gpt.enums import TalkGPTCommandOptions
from talk_gpt.gpt.models import Message
from talk_gpt.store.factory import RepositoryFactory

app = FastAPI()
talk_gpt = TalkGPT(
    cmd=TalkGPTCommandOptions.API, repository=RepositoryFactory.factory()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextToSpeech(BaseModel):
    content: str


@app.post("/upload", status_code=204)
async def upload(file: UploadFile) -> None:
    with open(VOICE_FROM_FILE, "wb") as f:
        f.write(file.file.read())


@app.post("/chat/text-to-speech")
async def chat_text_to_speech(tts: TextToSpeech) -> StreamingResponse:
    fp = text_to_speech(text=tts.content)
    return StreamingResponse(fp, media_type="audio/mp3")


@app.post("/chat/speech-to-text")
async def chat_speech_to_text(file: UploadFile) -> Message:
    content = speech_to_text(file=file)
    return Message(role="user", content=content)


@app.post("/chat/message")
async def chat_message(message: Message) -> Message:
    talk_gpt.send_message(message=message)
    return talk_gpt.present_ai_response()


@app.get("/chat/message/history")
async def chat_message_history() -> list[Message]:
    return talk_gpt._messages
