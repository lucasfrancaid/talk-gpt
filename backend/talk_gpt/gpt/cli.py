import time

import click
from openai.error import APIConnectionError, RateLimitError, ServiceUnavailableError

from talk_gpt.audio.speech import get_content, play_content
from talk_gpt.config.settings import settings
from talk_gpt.gpt.chat import TalkGPT
from talk_gpt.gpt.enums import CommandOption, PromptOption
from talk_gpt.gpt.models import Message, Role
from talk_gpt.store.chat.repository import ChatRepository


class TalkGPTCLI:
    def __init__(
        self,
        *,
        cmd: CommandOption,
        prompt: PromptOption,
        repository: ChatRepository,
        chat_id: str | None,
        reset: bool | None,
    ) -> None:
        self._talk_gpt = TalkGPT(cmd=cmd, prompt=prompt, repository=repository, chat_id=chat_id, reset=reset)
        self._is_voice_mode = cmd == CommandOption.VOICE
        self._should_play_audio = cmd in (CommandOption.AUDIO, CommandOption.VOICE)
        self._english_teacher_mode = prompt == PromptOption.ENGLISH_TEACHER

    def process(self):
        self._greetings()
        start_message = self._request_message()
        self._talk_gpt.send_message(message=start_message)
        self._print_response()

        retry = False
        while True:
            if not retry:
                message = self._request_message()

            try:
                self._talk_gpt.send_message(message=message)
                retry = False
                self._print_response()

            except (APIConnectionError, RateLimitError, ServiceUnavailableError) as e:
                retry = True
                click.echo(ClickStyle.ERROR.format(message=f"\nException error: {e}\n"))

                if hasattr(e, "should_retry"):
                    click.echo(ClickStyle.WARNING.format(message="--> Retrying based on OpenAI recommendation..."))
                    continue

                click.echo(ClickStyle.WARNING.format(message="--> Waiting for 2 seconds to retry"))
                time.sleep(2)
                click.echo(ClickStyle.WARNING.format(message="--> Retrying..."))

    def _greetings(self) -> None:
        if messages := self._talk_gpt.present_messages():
            click.echo(ClickStyle.WELCOME.format(message="Welcome back to TalkGPT."))
            for message in messages:
                self._print_message(message=message)
        elif self._english_teacher_mode:
            click.echo(ClickStyle.WELCOME.format(message="Welcome to TalkGPT, focused to improve your english."))
            english_teacher_name = (
                "" if settings.AI_ASSISTANT_NAME == "AI" 
                else f"{settings.AI_ASSISTANT_NAME.title()} "
            )
            click.echo(f"\nPresent yourself to {english_teacher_name}your AI English Teacher.")
        else:
            click.echo(ClickStyle.WELCOME.format(message="Welcome to TalkGPT."))
            click.echo("\nType what to you want to ask to ChatGPT")

    def _print_message(self, *, message: Message) -> None:
        style = ClickStyle.USER if message.role == "user" else ClickStyle.ASSISTANT
        click.echo(f"\n{style.format(label=message.role_to_str())}: {message.content}")

    def _request_message(self) -> Message:
        if not self._is_voice_mode:
            content = None
            while not content:
                content = click.prompt(ClickStyle.USER.format(label="\nYou"))
            message = Message(role=Role.USER, content=content)        
            return message

        message = Message(role=Role.USER, content=get_content())
        self._print_message(message=message)
        return message

    def _print_response(self) -> None:
        last_message = self._talk_gpt.present_ai_response()
        self._print_message(message=last_message)
        if self._should_play_audio:
            click.echo("\n")
            play_content(content=last_message.content)


class ClickStyle:
    WELCOME: str = click.style("{message}", bg="green", bold=True)
    USER: str = click.style("{label}", fg="green", bold=True)
    ASSISTANT: str = click.style("{label}", fg="blue", bold=True)
    WARNING: str = click.style("{message}", fg="yellow")
    ERROR: str = click.style("{message}", fg="red")
