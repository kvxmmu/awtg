from awtg.api import Telegram


tg = Telegram('token', proxy="proxy",
              message_callback=lambda x: None)

tg.poll(timeout=40)

