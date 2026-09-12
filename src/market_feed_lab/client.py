from websockets.asyncio.client import connect

from market_feed_lab.orderbook import FeedState
from market_feed_lab.protocol import Snapshot, decode_message


async def consume_feed(uri: str) -> FeedState:
    state = FeedState()

    async with connect(uri) as connection:
        async for raw in connection:
            message = decode_message(raw)

            if isinstance(message, Snapshot):
                state.load_snapshot(message.sequence)
                continue

            state.apply_update(message.sequence)

    return state
