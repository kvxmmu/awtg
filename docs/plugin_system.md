# AWTG's plugin system

When you need fully automated and scalable system(for bot, scalable means that you can easily add/remove commands/actions), plugins system is your choice.

Code for plugin system is in awtg.filtering package.

Example architecture:

```text
plugins:
    -- __init__.py
    -- test.py
main.py
```

main.py:
```python
from awtg.filtering.manager import Manager
from awtg.filtering.plugin_extractors import extract_from_dir

from awtg.api import Telegram

TOKEN = ''

tg = Telegram(TOKEN)
manager = Manager()

plugins = extract_from_dir('plugins')  # sample output: [<module 'plugins.test' from 'plugins dir'>

tg.set_callback(manager)  # Manager is plugin management system base class
manager.import_plugins(plugins)

tg.poll()
```

test.py:
```python
from awtg.filtering.manager import AsyncHandler


@AsyncHandler
async def do_responde(message):
    message.send('Quack')  # i stole it!


exports = (
    do_responde.add_filters(
        lambda message: message.data.get_text() == 'quack'
    ),
)
```

go open telegram and test this example!
