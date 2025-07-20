import asyncio
import logging

import typer

from telentfy import NotificationError, Notifier, TelentfySettings, __version__

app = typer.Typer()

logger = logging.getLogger(__name__)


@app.callback()
def main_callback(
    ctx: typer.Context, debug: bool = typer.Option(False, "--debug", help="Enable debug mode")
):
    settings = TelentfySettings()
    # Set up logging globally based on debug flag
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")
    logging.debug("debug mode is enabled")
    if log_level == logging.DEBUG:
        settings.DEBUG = True
    # Store settings in context for access in subcommands
    ctx.obj = {"settings": settings}


@app.command()
def version() -> None:
    print(__version__)


@app.command()
def ping(ctx: typer.Context, topic: str | None = None) -> None:
    if topic:
        ctx.obj["settings"].NTFY_TOPIC = topic
    logger.debug(f"pinging topic {ctx.obj['settings'].NTFY_TOPIC}")
    notifier = Notifier(ctx.obj["settings"])
    asyncio.run(notifier.send_notification("pong"))


def main() -> None:
    try:
        app()
    except NotificationError as ne:
        logger.error(ne)
