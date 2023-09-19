import click

from talk_gpt.gpt.enums import CommandOption, PromptOption


@click.command(help="Talk GPT - CLI to talk with ChatGPT")
@click.option(
    '-c', '--cmd', default="cli", help="Choose the conversation mode",
    type=click.Choice(tuple(option.value for option in CommandOption))
)
@click.option(
    '-p', '--prompt', default="gpt", help="Choose the prompt mode",
    type=click.Choice(tuple(option.value for option in PromptOption))
)
@click.option('-e', '--env-file', default=".env", help="Environment variables configuration file", type=str)
@click.option('-k', '--openai-key', help="OpenAI API key", type=str)
@click.option('-o', '--openai-org', help="OpenAI Organization", type=str)
@click.option('-n', '--ai-name', help="Choose your AI Name", type=str)
@click.option('-u', '--username', help="Choose your username", type=str)
@click.option('-id', '--chat-id', help="Create or load an existent chat by id", type=str)
@click.option(
    '-r', '--reset', is_flag=True, default=False,
    help="Reset your chat (based on cmd and prompt options)", type=bool
)
def main(
    cmd: str,
    prompt: str,
    env_file: str | None,
    openai_key: str | None,
    openai_org: str | None,
    ai_name: str | None,
    username: str | None,
    chat_id: str | None,
    reset: bool | None,
) -> None:
    import talk_gpt.config.settings as settings_file
    settings_file.settings = settings_file.Settings(env_file=env_file)

    if openai_key:
        settings_file.settings.OPENAI_KEY = openai_key
    if openai_org:
        settings_file.settings.OPENAI_ORG = openai_org
    if ai_name:
        settings_file.settings.AI_ASSISTANT_NAME = ai_name
    if username:
        settings_file.settings.USER_NAME = username

    from talk_gpt.gpt.cli import TalkGPTCLI
    from talk_gpt.store.factory import ChatRepositoryFactory

    cmd = CommandOption(cmd)
    if cmd == CommandOption.API:
        from talk_gpt.server import main as server
        return server.callback(env_file=env_file, skip_config=True)

    cli = TalkGPTCLI(
        cmd=CommandOption(cmd),
        prompt=PromptOption(prompt),
        repository=ChatRepositoryFactory.factory(),
        chat_id=chat_id,
        reset=reset,
    )
    cli.process()


if __name__ == "__main__":
    main()
