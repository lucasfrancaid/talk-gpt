import os
import time
from io import BytesIO

import speech_recognition as sr
from fastapi import UploadFile
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from speak_gpt.config.settings import ROOT_DIR

MEDIA_DIR = f"{ROOT_DIR}/etc/_media"
AUDIO_FILE = f"{MEDIA_DIR}/audio.mp3"
VOICE_FILE_EXT = "wav"
VOICE_FILE = f"{MEDIA_DIR}/voice.{VOICE_FILE_EXT}"
VOICE_FROM_FILE = f"{MEDIA_DIR}/rawvoice.{VOICE_FILE_EXT}"


def text_to_speech(*, text: str) -> BytesIO:
    tts = gTTS(text=text, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp=fp)
    fp.seek(0)
    return fp


def speech_to_text(*, file: UploadFile) -> str:
    filename = (
        f'{"".join(file.filename.split(".")[:-1])}.{VOICE_FILE_EXT}'
        if file.filename
        else VOICE_FILE
    )
    try:
        AudioSegment.from_file(file=file.file).export(filename, format=VOICE_FILE_EXT)
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = r.record(source=source)
            content = r.recognize_google(audio).capitalize()  # type: ignore
            return content
    finally:
        os.remove(filename)


def play_content(*, content: str) -> None:
    tts = gTTS(text=content, lang="en")
    tts.save(AUDIO_FILE)
    sound = AudioSegment.from_mp3(AUDIO_FILE)
    play(sound)


def get_content() -> str:
    exception_retries = 0
    while True:
        try:
            AudioSegment.from_file(VOICE_FROM_FILE).export(
                VOICE_FILE, format=VOICE_FILE_EXT
            )
            os.remove(VOICE_FROM_FILE)

            r = sr.Recognizer()
            with sr.AudioFile(VOICE_FILE) as source:
                audio = r.record(source=source)
                content = r.recognize_google(audio).capitalize()  # type: ignore

            print(f"\nRecorded: {content}")
            is_valid_record = input("\n--> Recorded message is valid? (y/n): ")
            if is_valid_record.lower() in ("n", "no", "not"):
                exception_retries = 0
                continue

            return content

        except FileNotFoundError:
            if exception_retries == 108:
                exit()
            print("\n--> Record an audio in the client to send a message")
            time.sleep(5)
            exception_retries += 1


# def record_and_get_content() -> str:
#     r = sr.Recognizer()
#     # Need to install pyaudio
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         print("Talk something")
#         audio_text = r.listen(source)
#         print("Finished")
#         content = r.recognize_google(audio_text)
#         return content


# def _list_mic():
#     import speech_recognition as sr
#     # Need to install pyaudio
#     for index, name in enumerate(sr.Microphone.list_microphone_names()):
#         print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))


if __name__ == "__main__":
    content = get_content()
    print(content)
