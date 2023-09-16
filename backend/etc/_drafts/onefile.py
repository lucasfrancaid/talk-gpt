import argparse
import os
import time

import openai
import speech_recognition as sr
from gtts import gTTS
from openai.error import APIConnectionError, RateLimitError, ServiceUnavailableError
from pydub import AudioSegment
from pydub.playback import play

GPT_MODEL = "gpt-3.5-turbo"
VOICE_FROM_FILE = ""
VOICE_FILE = ""
VOICE_FILE_EXT = ""

openai.api_key = ""
openai.organization = ""

_messages = []


def play_content(*, content: str) -> None:
    tts = gTTS(text=content, lang="en")
    tts.save("audio.mp3")
    sound = AudioSegment.from_mp3("audio.mp3")
    play(sound)


def get_content() -> str:
    exception_retries = 0
    while True:
        try:
            AudioSegment.from_file(VOICE_FROM_FILE).export(VOICE_FILE, format=VOICE_FILE_EXT)
            os.remove(VOICE_FROM_FILE)

            r = sr.Recognizer()
            with sr.AudioFile(VOICE_FILE) as source:
                audio = r.record(source=source)
                content = r.recognize_google(audio).capitalize()

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


def input_content(*, voice_mode: bool) -> str:
    if not voice_mode:
        content = input("\n--> Type here: ")
        return content
    content = get_content()
    print(f"\nUser: {content}\n")
    return content


def generate_message(*, role: str, content: str) -> dict:
    return {
        "role": role,
        "content": content
    }


def append_ai_message(*, message):
    _messages.append(generate_message(role=message.role, content=message.content))


def chat_completion_process():
    chat_completion = openai.ChatCompletion.create(model=GPT_MODEL, messages=_messages)
    append_ai_message(message=chat_completion.choices[0].message)


def print_last_message(play_audio: bool = False):
    last_message = _messages[-1]
    print(f"\n{last_message['role'].title()}: {last_message['content']}")
    if play_audio:
        print("\n")
        play_content(content=last_message['content'])


def main(voice_mode: bool = False):
    print("--> Welcome to SpeakGPT, focused to improve your english. \n")
    print("Present yourself to AI English Teacher. \n")

    first_content = input_content(voice_mode=voice_mode)

    extended_context = "" if not voice_mode else (
        "Don't reply with prompts, each reply must be a message and this message will be transcripted to "
        "audio, so return the message formatted to it. Sometimes I will ask for a mock converstion about "
        "specific topics, so you need to handle with it just through messages and not returning prompts."
    )

    _messages.extend([
        generate_message(role="system", content=(
            "You are an AI English Teacher focused in conversational study with British accent. "
            "This chat must looks like a real conversation between student and teacher. {extended_context}"
            "Another thing you must be is, when I make some mistake in my sentence you need to correct me "
            "saying what I did wrong and explaining the correct way. \n\n"
        ).format(extended_context=extended_context)),
        generate_message(role="user", content=first_content),
    ])
    print_last_message(play_audio=False)

    chat_completion_process()
    while True:
        print_last_message(play_audio=voice_mode)
        content = input_content(voice_mode=voice_mode)
        _messages.append(generate_message(role="user", content=content))

        try:
            print("\n--> Processing message...")
            chat_completion_process()
        except (APIConnectionError, RateLimitError, ServiceUnavailableError) as e:
            print(str(e))
            if getattr(e, "should_retry", None):
                print("\n--> Retrying based on OpenAI recommendation...")
                continue

            print("\n--> Sleeping for 5 seconds to retry")
            time.sleep(5)
            print("\n--> Retrying by myself...")


parser = argparse.ArgumentParser(description="Speak GPT - CLI to interact with ChatGPT")
parser.add_argument("-c", "--cmd", default="cli", choices=("cli", "voice"), help="Command talk mode")
args = parser.parse_args()
is_voice_mode = args.cmd == "voice"
main(voice_mode=is_voice_mode)
