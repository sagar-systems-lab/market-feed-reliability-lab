from collections.abc import Awaitable, Callable, Iterable

from websockets.asyncio.server import ServerConnection

from market_feed_lab.protocol import FeedMessage, encode_message


async def send_feed(
    connection: ServerConnection,
    messages: Iterable[FeedMessage],
) -> None:
    for message in messages:
        await connection.send(encode_message(message))


def make_feed_handler(
    messages: Iterable[FeedMessage],
) -> Callable[[ServerConnection], Awaitable[None]]:
    feed = tuple(messages)

    async def handler(connection: ServerConnection) -> None:
        await send_feed(connection, feed)

    return handler
