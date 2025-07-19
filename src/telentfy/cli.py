import asyncio
import logging

import typer

from telentfy import Notifier, TelentfySettings, __version__

app = typer.Typer()

logger = logging.getLogger(__name__)


@app.command()
def version() -> None:
    print(__version__)


@app.command()
def ping(topic: str | None = None) -> None:
    settings = TelentfySettings()
    if topic:
        settings.NTFY_TOPIC = topic
    logger.debug(f"pinging topic {settings.NTFY_TOPIC}")
    notifier = Notifier(settings)
    asyncio.run(notifier.send_notification("pong"))


def main() -> None:
    app()
