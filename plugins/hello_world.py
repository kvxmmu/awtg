from awtg.filtering.manager import AsyncHandler, async_decorator
from awtg.filtering.std import Prefix, Command


@AsyncHandler
async def test(message):
    message.send("Match by prefix")


@AsyncHandler
async def test2(message):
    message.send("Hello world request")


@async_decorator(
    Command("test_decorator"))
async def async_decorator_test(message):
    message.send("Async decorator test")


exports = (
    test2.add_filter(
        Command("get_hello_world")
    ),

    test.add_filter(
        Prefix(r"aw\s*")
    ),

    async_decorator_test
)

