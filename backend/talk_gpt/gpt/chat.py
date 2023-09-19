from datetime import datetime

import openai
from openai.error import OpenAIError

from talk_gpt.config.settings import settings
from talk_gpt.gpt.enums import CommandOption, PromptOption
from talk_gpt.gpt.models import Message, Role
from talk_gpt.store.chat.repository import ChatRepository

openai.api_key = settings.OPENAI_API_KEY
openai.organization = settings.OPENAI_ORGANIZATION


class TalkGPT:
    def __init__(
        self,
        *,
        cmd: CommandOption,
        prompt: PromptOption,
        repository: ChatRepository,
        chat_id: str | None = None,
        reset: bool = False,
    ) -> None:
        self._cmd = cmd
        self._prompt = prompt
        self._repository = repository
        self._chat_id = chat_id or self._build_chat_id()
        self._messages = self._initilize_messages(reset=reset)

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
        self._repository.save(chat_id=self._chat_id, messages=self._messages)

    def present_messages(self) -> list[Message]:
        if self._messages and self._messages[0].role == Role.SYSTEM:
            return self._messages[1:]
        return self._messages

    def present_ai_response(self) -> Message:
        last_message = self._messages[-1]
        return last_message

    def _initilize_messages(self, *, reset: bool) -> list[Message]:
        messages = []
        if not reset and (stored_messages := self._repository.read(chat_id=self._chat_id)):
            messages.extend(stored_messages)

        if not messages:
            self._set_prompt_context(messages=messages)

        self._repository.save(chat_id=self._chat_id, messages=messages)
        return messages

    def _set_prompt_context(self, *, messages: list[Message]) -> None:
        voice_context = (
            ""
            if self._cmd not in (CommandOption.API, CommandOption.VOICE)
            else (
                "Don't reply with prompts, each reply must be a message and this message will be transcripted to "
                "audio, so return the message formatted to it. Sometimes I will ask for a mock converstion about "
                "specific topics, so you need to handle with it just through messages and not returning prompts."
            )
        )

        match self._prompt:
            case PromptOption.ENGLISH_TEACHER:
                ai_name_context = (
                    "" if settings.AI_ASSISTANT_NAME == "AI"
                    else f" and your name is {settings.AI_ASSISTANT_NAME}"
                )
                messages.append(Message(
                    role=Role.SYSTEM,
                    content=(
                        f"You are an AI English Teacher{ai_name_context}. "
                        "This chat should resemble a real conversation between a student and a teacher. "
                        "You should be aware that when I make mistakes in language, you should correct me, "
                        "telling me what I did wrong and explaining how to do it correctly."
                        f"\n{voice_context}"
                    ),
                ))
            case PromptOption.GPT:
                if voice_context:
                    messages.append(Message(role=Role.SYSTEM, content=voice_context))

    def _build_chat_id(self) -> str:
        today = datetime.now().strftime('%d%m%Y')
        return f"{self._cmd.value}_{self._prompt.value}_{today}"
