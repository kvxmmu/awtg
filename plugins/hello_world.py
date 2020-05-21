from awtg.filtering.manager import AsyncHandler
from awtg.filtering.std import Prefix, Command


@AsyncHandler
async def test(message):
    message.send("Match by prefix")


@AsyncHandler
async def test2(message):
    message.send("Hello world request")


exports = (
    test2.add_filter(
        Command("get_hello_world")
    ),

    test.add_filter(
        Prefix(r"aw\s*")
    )
)

