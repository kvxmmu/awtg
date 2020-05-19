from inspect import iscoroutine


class AsyncHandler:
    def __init__(self, callback):
        self.callback = callback
        self.filters = []

    @staticmethod
    def is_optional(func):
        return hasattr(func, '__optional__') and func.__optional__

    async def __call__(self, message):
        for filter_ in self.filters:
            response = filter_(message)

            if iscoroutine(response):
                response = await response

            if not response and not self.is_optional(filter_):
                return
        message.tg.loop.create_task(self.callback(message))
