import click
import uvicorn


@click.command(help="Talk GPT - API")
@click.option('-e', '--env-file', default=".env", help="Environment variables configuration file", type=str)
def main(env_file: str | None, skip_config: bool = False):
    import talk_gpt.config.settings as settings_file

    settings = settings_file.settings

    if not skip_config:
        settings = settings_file.settings = settings_file.Settings(env_file=env_file)

    from talk_gpt.router.main import app

    config = uvicorn.Config(
        app=app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level="debug" if settings.DEBUG else "info",
        # ssl_keyfile="/certs/key.pem",
        # ssl_certfile="/certs/certificate.pem",
    )
    server = uvicorn.Server(config=config)
    server.run()


if __name__ == "__main__":
    main()
