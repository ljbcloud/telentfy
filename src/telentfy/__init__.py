import importlib.metadata

from telentfy.notifier import NotificationError, Notifier
from telentfy.settings import TelentfySettings

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.5"

__all__ = ["NotificationError", "Notifier", "TelentfySettings"]
