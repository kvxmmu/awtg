from inspect import iscoroutine
from importlib import import_module

from functools import partial


async def check_filter(message, filters):
    for filter_ in filters:
        response = filter_(message)

        if iscoroutine(response):
            response = await response

        if not response and not AsyncHandler.is_optional(filter_):
            return False
    return True


class AsyncHandler:

    __optional__ = True

    def __init__(self, callback):
        self.callback = callback
        self.filters = []

    @staticmethod
    def is_optional(func):
        return hasattr(func, '__optional__') and func.__optional__

    def set_optional(self, value=True):
        self.__optional__ = value
        return self

    def add_filter(self, filter_):
        self.filters.append(filter_)
        return self

    def add_filters(self, *filters):
        self.filters.extend(filters)
        return self

    def __call__(self, message):
        callback_data = self.callback(message)

        if iscoroutine(callback_data):
            return message.tg.loop.create_task(callback_data)

        return callback_data


class Manager:
    def __init__(self, default_filters=None):
        if default_filters is None:
            default_filters = []

        self.default_filters = default_filters
        self.handlers = []

    def import_plugin(self, plugin):
        self.handlers.extend(plugin.exports)

    def import_handler(self, handler):
        self.handlers.append(handler)

    def import_plugin_module(self, name):
        module = import_module(name)
        assert hasattr(module, 'exports')

        self.import_plugin(module)

    async def __call__(self, message):
        default_check = await check_filter(message, self.default_filters)

        if not default_check:
            return

        for handler in self.handlers:
            response = await check_filter(message, handler.filters)
            optional = AsyncHandler.is_optional(handler)

            if not response and optional:
                continue
            elif not response and not optional:
                return

            handler(message)


def create_async_handler(filters, optional, handler):
    if not filters:
        filters = ()

    async_handler = AsyncHandler(handler).add_filters(*filters).set_optional(optional)

    return async_handler


def async_decorator(*filters, optional=True):
    return partial(create_async_handler, filters, optional)

