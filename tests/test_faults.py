from websockets.asyncio.server import serve

from market_feed_lab.client import consume_feed
from market_feed_lab.faults import duplicate_at, drop_at, swap_adjacent
from market_feed_lab.protocol import Snapshot, Update
from market_feed_lab.server import make_feed_handler


async def consume(messages):
    async with serve(
        make_feed_handler(messages),
        "127.0.0.1",
        0,
    ) as server:
        port = server.sockets[0].getsockname()[1]
        return await consume_feed(f"ws://127.0.0.1:{port}")


async def test_duplicate_update_is_tolerated_over_transport():
    messages = [
        Snapshot(sequence=100),
        Update(sequence=101),
        Update(sequence=102),
    ]

    state = await consume(duplicate_at(messages, 1))

    assert state.valid
    assert state.last_sequence == 102
    assert state.applied_updates == 2
    assert state.duplicates == 1


async def test_dropped_update_invalidates_state():
    messages = [
        Snapshot(sequence=100),
        Update(sequence=101),
        Update(sequence=102),
        Update(sequence=103),
    ]

    state = await consume(drop_at(messages, 2))

    assert not state.valid
    assert state.last_sequence == 101
    assert state.invalidations == 1


async def test_reordered_update_invalidates_state():
    messages = [
        Snapshot(sequence=100),
        Update(sequence=101),
        Update(sequence=102),
        Update(sequence=103),
    ]

    state = await consume(swap_adjacent(messages, 2))

    assert not state.valid
    assert state.last_sequence == 101
    assert state.invalidations == 1
