from awtg.api import Telegram
from awtg.filtering.manager import Manager

manager = Manager()
manager.import_plugin_module("plugins.hello_world")


tg = Telegram("x", proxy="y",
              message_callback=manager)

tg.poll(timeout=40)

