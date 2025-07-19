import asyncio
import logging
from typing import Any, Optional, Self

import aiohttp

from telentfy.settings import TelentfySettings

logger = logging.getLogger(__name__)


class NotificationError(Exception):
    pass


class Notifier:
    def __init__(
        self: Self,
        settings: Optional[TelentfySettings] = None,
        write_log: bool = True,
    ):
        if settings:
            self.settings = settings
        else:
            self.settings = TelentfySettings()

        if self.ntfy_enabled:
            logger.info("ntfy notifications enabled")

        if self.telegram_enabled:
            logger.info("telegram notifications enabled")

        self.write_log = write_log

    @property
    def ntfy_enabled(self: Self) -> bool:
        return bool(self.settings.NTFY_URL and self.settings.NTFY_TOPIC)

    @property
    def telegram_enabled(self: Self) -> bool:
        return bool(self.settings.TELEGRAM_API_KEY and self.settings.TELEGRAM_CHAT_ID)

    async def _post(
        self: Self,
        url: str,
        data: dict[str, Any],
    ) -> Any:
        headers = {"Content-Type": "application/json"}
        try:
            async with (
                aiohttp.ClientSession() as session,
                session.post(url, headers=headers, json=data) as response,
            ):
                if response.status != 200:
                    error_text = await response.text()
                    raise NotificationError(
                        f"Failed to send message. status: {response.status}, \
                            response: {error_text}"
                    )

                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"network error when sending message: {e!s}")
            raise NotificationError(f"network error: {e!s}") from e
        except asyncio.TimeoutError as e:
            logger.error("timeout error when sending message")
            raise NotificationError("request timed out") from e
        except Exception as e:
            logger.error(f"unexpected error when sending message: {e!s}")
            raise NotificationError(f"unexpected error: {e!s}") from e

    async def send_notification(self: Self, message: str, log_level: int = logging.INFO) -> None:
        if self.telegram_enabled:
            await self.notify_telegram(message, log_level)
        if self.ntfy_enabled:
            await self.notify_ntfy(message, log_level)

    async def notify_ntfy(self: Self, message: str, log_level: int = logging.INFO) -> None:
        logger.log(msg=f"sending notification: {message}", level=log_level)
        await self._post(
            self.settings.NTFY_URL,
            data={"topic": self.settings.NTFY_TOPIC, "message": message},
        )

    async def notify_telegram(self: Self, message: str, log_level: int = logging.INFO) -> None:
        logger.log(msg=f"sending telegram notification: {message}", level=log_level)
        await self._post(
            f"https://api.telegram.org/bot{self.settings.TELEGRAM_API_KEY}/sendMessage",
            {
                "chat_id": self.settings.TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_notification": True,
            },
        )
