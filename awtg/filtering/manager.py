from inspect import iscoroutine
from inspect import signature
from importlib import import_module

from functools import partial
from copy import copy

from awtg.types import CallbackQueryHandler, Message
from awtg.storage import MessagesPool


async def check_filter(message, filters,
                       manager):
    for filter_ in filters:
        filter_args = get_function_arguments(filter_)

        if len(filter_args) == 2:
            response = filter_(message, manager)
        elif len(filter_args) == 1:
            response = filter_(message)
        else:
            raise ValueError('Invalid filter signature')

        if iscoroutine(response):
            response = await response

        if not response and not getattr(filter_, '__optional__', False):
            return False
    return True


def get_function_arguments(func):
    return list(signature(func).parameters)


class AsyncHandler:

    __optional__ = True
    __callback__ = False
    __every_message_handler__ = False

    def __init__(self, callback):
        self.callback = callback
        self.filters = []
        self.mutual_callbacks = []

        self.await_callbacks = True

    @staticmethod
    def is_optional(func):
        return getattr(func, '__optional__', AsyncHandler.__optional__)

    @staticmethod
    def is_callback(func):
        return getattr(func, '__callback__', False)

    @staticmethod
    def is_every_message_handler(func):
        return getattr(func, '__every_message_handler__', False)

    def set_optional(self, value=True):
        self.__optional__ = value
        return self

    def set_callback(self, value=True):
        self.__callback__ = value

        return self

    def set_every_message_handler(self, value=True):
        self.__every_message_handler__ = value

        return self

    def set_await_callbacks(self, value=False):
        self.await_callbacks = value

    def add_filter(self, filter_):
        self.filters.append(filter_)

        return self

    def add_filters(self, *filters):
        self.filters.extend(filters)

        return self

    def add_mutual_callback(self, callback):
        self.mutual_callbacks.append(callback)

        return self

    def add_mutual_callbacks(self, *callbacks):
        self.mutual_callbacks.extend(callbacks)

        return self

    def copy(self):
        return copy(self)

    async def __call__(self, message, manager):
        for callback in self.mutual_callbacks:
            callback_args = get_function_arguments(callback)

            if len(callback_args) == 2:
                response = callback(message, manager)
            elif len(callback_args) == 1:
                response = callback(callback_args)
            else:
                raise ValueError('Invalid filter signature')

            if iscoroutine(response):
                if self.await_callbacks:
                    await response
                else:
                    message.tg.loop.create_task(response)

        callback_data = self.callback(message)

        if iscoroutine(callback_data):
            return message.tg.loop.create_task(callback_data)

        return callback_data


class Manager:
    def __init__(self, default_message_filters=None,
                 default_callback_filters=None):
        if default_message_filters is None:
            default_message_filters = []

        if default_callback_filters is None:
            default_callback_filters = []

        self.default_message_filters = default_message_filters
        self.default_callback_filters = default_callback_filters

        self.handlers = []

        self.messages_pool = None

    def import_plugin(self, plugin):
        self.handlers.extend(plugin.exports)

    def require_messages_pool(self, *args, **kwargs):
        self.messages_pool = MessagesPool(*args, **kwargs)

    def import_handler(self, handler):
        self.handlers.append(handler)

    def import_plugin_module(self, name):
        module = import_module(name)
        assert hasattr(module, 'exports')

        self.import_plugin(module)

    def import_plugins(self, plugins):
        for plugin in plugins:
            self.import_plugin(plugin)

    async def __call__(self, entity):
        assert isinstance(entity, Message) or isinstance(entity, CallbackQueryHandler)

        filters_list = self.default_message_filters

        if isinstance(entity, CallbackQueryHandler):
            filters_list = self.default_callback_filters

        default_check = await check_filter(entity, filters_list,
                                           self)

        if not default_check:
            return

        for handler in self.handlers:
            if not AsyncHandler.is_callback(handler) and isinstance(entity, CallbackQueryHandler):
                continue
            elif AsyncHandler.is_callback(handler) and isinstance(entity, Message):
                continue

            if AsyncHandler.is_every_message_handler(handler):
                entity.tg.loop.create_task(handler(entity, self))
                continue

            response = await check_filter(entity, handler.filters,
                                          self)
            optional = AsyncHandler.is_optional(handler)

            if not response and optional:
                continue
            elif not response and not optional:
                return

            entity.tg.loop.create_task(handler(entity, self))


def create_async_handler(filters, optional, handler):
    if not filters:
        filters = ()

    async_handler = AsyncHandler(handler).add_filters(*filters).set_optional(optional)

    return async_handler


def async_decorator(*filters, optional=True):
    return partial(create_async_handler, filters, optional)

