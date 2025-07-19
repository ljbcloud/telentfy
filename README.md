# telentfy

Library for sending simple text notifications to [ntfy.sh][] and [Telegram][] channels.

## Installation

```shell
pip install telentfy==0.0.3
```

## Usage

### CLI

```shell
# print the currently installed version
telentfy version

# send a ping to all configured channels/topics
telentfy ping
```

### Library

```python
from telentfy import Notifier, TelentfySettings

# load settings from environment (e.g. .env)
settings = TelentfySettings()
# override environment
settings.NTFY_TOPIC = "testing123"
settings.NTFY_URL = "https://ntfy.sh"

notifier = Notifier(settings)

notifier.send_notification("ping")
```

<!-- References -->
[ntfy.sh]: <https://ntfy.sh>
[Telegram]: <https://telegram.org>
