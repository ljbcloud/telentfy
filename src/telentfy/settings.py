from typing import Any, Optional, Self

from pydantic_settings import BaseSettings, SettingsConfigDict


class TelentfySettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    def __init__(self: Self, env_file: str = ".env", env_prefix: str = "TELENTFY_", **values: Any):
        super().__init__(_env_file=env_file, _env_prefix=env_prefix)

    # ntfy
    NTFY_URL: str = "https://ntfy.sh"
    NTFY_TOPIC: Optional[str] = None

    # telegram
    TELEGRAM_CHAT_ID: Optional[str] = None
    TELEGRAM_API_KEY: Optional[str] = None
