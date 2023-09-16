import argparse

from speak_gpt.gpt.cli import SpeakGPTCLI
from speak_gpt.gpt.enums import SpeakGPTCommandOptions
from speak_gpt.store.factory import RepositoryFactory


def main():
    parser = argparse.ArgumentParser(
        description="Speak GPT - CLI to interact with ChatGPT"
    )
    parser.add_argument(
        "-c",
        "--cmd",
        default="cli",
        choices=("cli", "audio", "voice"),
        help=(
            "This flag is to choose the command talk mode. \n"
            "The different options provide different experiences: \n"
            "- cli: It is a chat conversation, you will read and write your conversation with AI. \n"
            "- audio: It is a hybrid conversation, you will write your message but you will read and listen from AI. \n"
            "- voice: It is a speak conversation, you will record voice messages and will listen from AI. \n"
        ),
    )
    args = parser.parse_args()
    cli = SpeakGPTCLI(
        cmd=SpeakGPTCommandOptions(args.cmd), repository=RepositoryFactory.factory()
    )
    cli.process()


if __name__ == "__main__":
    main()
