import time

from openai.error import APIConnectionError, RateLimitError, ServiceUnavailableError

from speak_gpt.audio.speech import get_content, play_content
from speak_gpt.gpt.chat import SpeakGPT
from speak_gpt.gpt.enums import SpeakGPTCommandOptions
from speak_gpt.gpt.models import Message
from speak_gpt.store.repository import Repository


class SpeakGPTCLI:
    def __init__(self, *, cmd: SpeakGPTCommandOptions, repository: Repository) -> None:
        self._cmd = cmd
        self._speak_gpt = SpeakGPT(cmd=cmd, repository=repository)
        self.is_voice_mode = self._cmd == SpeakGPTCommandOptions.VOICE
        self.should_play_audio = self._cmd in (
            SpeakGPTCommandOptions.AUDIO,
            SpeakGPTCommandOptions.VOICE,
        )

    def input_content(self) -> str:
        if not self.is_voice_mode:
            content = None
            while not content:
                content = input("\n--> Type here: ")
            return content
        content = get_content()
        print(f"\nUser: {content}\n")
        return content

    def print_response(self):
        last_message = self._speak_gpt.present_ai_response()
        print(f"\n{last_message.role.title()}: {last_message.content}")
        if self.should_play_audio:
            print("\n")
            play_content(content=last_message.content)

    def process(self):
        print("--> Welcome to SpeakGPT, focused to improve your english. \n")
        print("Present yourself to Kara your AI English Teacher. \n")

        first_message = Message(role="user", content=self.input_content())
        if self.is_voice_mode:
            print(f"\n{first_message.role.title()}: {first_message.content}")

        self._speak_gpt.send_message(message=first_message)

        while True:
            self.print_response()
            content = self.input_content()

            try:
                print("\n--> Processing message...")
                self._speak_gpt.send_message(
                    message=Message(role="user", content=content)
                )
                self.print_response()
            except (APIConnectionError, RateLimitError, ServiceUnavailableError) as e:
                print(str(e))
                if getattr(e, "should_retry", None):
                    print("\n--> Retrying based on OpenAI recommendation...")
                    continue

                print("\n--> Sleeping for 5 seconds to retry")
                time.sleep(5)
                print("\n--> Retrying by myself...")
