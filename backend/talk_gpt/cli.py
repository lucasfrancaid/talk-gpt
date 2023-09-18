import click

from talk_gpt.gpt.enums import TalkGPTCommandOptions


@click.command(help="Talk GPT - CLI to talk with ChatGPT")
@click.option(
    '-c', '--cmd', default="cli", help="Choose the conversation mode",
    type=click.Choice(tuple(option.value for option in TalkGPTCommandOptions))
)
@click.option('-e', '--env-file', default=".env", help="Environment variables configuration file", type=str)
@click.option('-k', '--openai-key', help="OpenAI API key", type=str)
@click.option('-o', '--openai-org', help="OpenAI Organization", type=str)
def main(cmd: str, env_file: str | None, openai_key: str | None, openai_org: str | None) -> None:
    import talk_gpt.config.settings as settings_file
    settings_file.settings = settings_file.Settings(env_file=env_file)

    if openai_key:
        settings_file.settings.OPENAI_KEY = openai_key
    if openai_org:
        settings_file.settings.OPENAI_ORG = openai_org

    from talk_gpt.gpt.cli import TalkGPTCLI
    from talk_gpt.store.factory import RepositoryFactory

    cli = TalkGPTCLI(cmd=TalkGPTCommandOptions(cmd), repository=RepositoryFactory.factory())
    cli.process()


if __name__ == "__main__":
    main()
