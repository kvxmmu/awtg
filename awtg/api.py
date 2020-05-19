from rapidjson import loads, dumps
from .types import (Updates, MessageData,
                    Message)
from dataclass_factory import Factory, Schema

import asyncio
import aiohttp

from inspect import iscoroutine


class Telegram:
    def __init__(self, bot_token, connector=None,
                 close_session=True, proxy=None,
                 message_callback=None):
        self.bot_token = bot_token
        self.session = aiohttp.ClientSession(connector=connector)
        self.close_session = close_session

        self.proxy = proxy

        self.loop = asyncio.get_event_loop()
        self.url = "https://api.telegram.org/bot%s/" % bot_token

        self.running = False

        self.factory = Factory(default_schema=Schema(trim_trailing_underscore=True))

        self.message_callback = message_callback

    async def method(self, method_name, params=None):
        if params is None:
            params = {}
        async with self.session.post(self.url+method_name, data=params, proxy=self.proxy) as response:
            return loads(await response.text())

    async def get_updates(self, offset, timeout,
                          limit):
        params = {'timeout': timeout, 'offset': offset,
                  'allowed_updates': '["message"]'}  # TODO: remove it

        if limit:
            params['limit'] = limit

        updates = await self.method("getUpdates", params)
        return self.factory.load(updates, Updates)

    async def process_message(self, update):
        if not self.message_callback:
            return  # skip update because message callback is not set
        msg = Message(update.message, self)
        cb_res = self.message_callback(msg)

        if iscoroutine(cb_res):
            await cb_res

    async def process_updates(self, updates):
        for update in updates.result:
            if update.message:
                self.loop.create_task(self.process_message(update))

    async def _loop(self, updates_limit, timeout):
        self.running = True

        offset = None

        while self.running:
            updates = await self.get_updates(offset, timeout, updates_limit)

            if updates.result:
                offset = updates.result[-1].update_id+1
                self.loop.create_task(self.process_updates(updates))

    def poll(self, updates_limit=None, timeout=None):
        self.loop.run_until_complete(self._loop(updates_limit, timeout))

    def __del__(self):
        if self.close_session:
            self.loop.run_until_complete(self.session.close())
