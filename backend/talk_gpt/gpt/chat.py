import openai
from openai.error import OpenAIError

from talk_gpt.config.settings import settings
from talk_gpt.gpt.enums import TalkGPTCommandOptions
from talk_gpt.gpt.models import Message
from talk_gpt.store.repository import Repository

openai.api_key = settings.OPENAI_API_KEY
openai.organization = settings.OPENAI_ORGANIZATION


class TalkGPT:
    def __init__(self, *, cmd: TalkGPTCommandOptions, repository: Repository) -> None:
        self._cmd = cmd
        self._repository = repository
        self._messages = self._initilize_messages()

    def _initilize_messages(self) -> list[Message]:
        voice_context = (
            ""
            if self._cmd not in (TalkGPTCommandOptions.API, TalkGPTCommandOptions.VOICE)
            else (
                "Don't reply with prompts, each reply must be a message and this message will be transcripted to "
                "audio, so return the message formatted to it. Sometimes I will ask for a mock converstion about "
                "specific topics, so you need to handle with it just through messages and not returning prompts."
            )
        )
        messages = [
            Message(
                role="system",
                content=(
                    "You are an AI English Teacher focused in conversational study with British accent and your name is Kara. "
                    "This chat must looks like a real conversation between student and teacher. {voice_context}"
                    "Another thing you must be is, when I make some mistake in my sentence you need to correct me "
                    "saying what I did wrong and explaining the correct way."
                ).format(voice_context=voice_context),
            )
        ]

        if stored_messages := self._repository.read():
            messages.extend(stored_messages[1:])
        self._repository.save(messages=messages)
        return messages

    def send_message(self, *, message: Message) -> None:
        try:
            chat_completion = openai.ChatCompletion.create(
                model=settings.GPT_MODEL,
                messages=[msg.dict() for msg in self._messages + [message]],
                timeout=60,
            )
            self._messages.append(message)
        except OpenAIError as exc:
            if hasattr(exc, "should_retry"):
                return self.send_message(message=message)
            raise exc

        ai_message = chat_completion.choices[0].message  # type: ignore
        self._messages.append(Message(role=ai_message.role, content=ai_message.content))
        self._repository.save(messages=self._messages)

    def present_ai_response(self) -> Message:
        last_message = self._messages[-1]
        return last_message
