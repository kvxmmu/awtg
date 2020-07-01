# AWTG base usage

See this example

```python
from awtg.api import Telegram

TOKEN = 'bot api token'

tg = Telegram(TOKEN)


@tg.set_message_callback
async def callback(message):
    message.send('Ok')

tg.poll()

```

idk why you need to use my library like that, but it's possible.

# Simple objects reference

```text
Telegram(bot_token, connector=None,
                 close_session=True, proxy=None,
                 message_callback=None)

connector - custom aiohttp connector
close_session - perform closing action on aiohttp session after Telegram is used and is being freed
message_callback - function that is being called when a new message arrives
proxy - aiohttp built-in supported proxies

Message object is defined in types.py:

signature:

def send(self, text=None, chat_id=None,
         reply=False, reply_message_id=None,
         parse_mode="html", disable_web_page_preview=False,
         disable_notification=False)

go to https://core.telegram.org/bots/api#sendmessage for fields description

Markups is not currently supported

```

