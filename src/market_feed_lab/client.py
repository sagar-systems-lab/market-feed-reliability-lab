from collections.abc import Iterable

from websockets.asyncio.client import connect

from market_feed_lab.orderbook import FeedState
from market_feed_lab.protocol import Snapshot, decode_message


async def consume_connection(
    uri: str,
    state: FeedState,
) -> FeedState:
    async with connect(uri) as connection:
        async for raw in connection:
            message = decode_message(raw)

            if isinstance(message, Snapshot):
                state.load_snapshot(message.sequence)
                continue

            state.apply_update(message.sequence)

    return state


async def consume_feed(uri: str) -> FeedState:
    state = FeedState()
    return await consume_connection(uri, state)


async def consume_sessions(uris: Iterable[str]) -> FeedState:
    state = FeedState()

    for session_index, uri in enumerate(uris):
        if session_index:
            state.invalidate()

        await consume_connection(uri, state)

    return state
