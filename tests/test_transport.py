from websockets.asyncio.server import serve

from market_feed_lab.client import consume_feed
from market_feed_lab.protocol import Snapshot, Update
from market_feed_lab.server import make_feed_handler


async def test_snapshot_and_updates_flow_over_websocket():
    messages = [
        Snapshot(sequence=100),
        Update(sequence=101),
        Update(sequence=102),
    ]

    async with serve(
        make_feed_handler(messages),
        "127.0.0.1",
        0,
    ) as server:
        port = server.sockets[0].getsockname()[1]

        state = await consume_feed(
            f"ws://127.0.0.1:{port}"
        )

    assert state.valid
    assert state.last_sequence == 102
    assert state.applied_updates == 2
