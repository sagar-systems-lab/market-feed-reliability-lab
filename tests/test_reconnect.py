from websockets.asyncio.server import serve

from market_feed_lab.client import consume_sessions
from market_feed_lab.protocol import Snapshot, Update
from market_feed_lab.server import make_feed_handler


def server_uri(server) -> str:
    port = server.sockets[0].getsockname()[1]
    return f"ws://127.0.0.1:{port}"


async def test_reconnect_without_snapshot_keeps_state_invalid():
    first_session = [
        Snapshot(sequence=100),
        Update(sequence=101),
    ]

    second_session = [
        Update(sequence=102),
        Update(sequence=103),
    ]

    async with (
        serve(make_feed_handler(first_session), "127.0.0.1", 0) as first,
        serve(make_feed_handler(second_session), "127.0.0.1", 0) as second,
    ):
        state = await consume_sessions(
            [
                server_uri(first),
                server_uri(second),
            ]
        )

    assert not state.valid
    assert state.last_sequence == 101
    assert state.invalidations == 1


async def test_fresh_snapshot_restores_state_after_reconnect():
    first_session = [
        Snapshot(sequence=100),
        Update(sequence=101),
    ]

    second_session = [
        Snapshot(sequence=200),
        Update(sequence=201),
    ]

    async with (
        serve(make_feed_handler(first_session), "127.0.0.1", 0) as first,
        serve(make_feed_handler(second_session), "127.0.0.1", 0) as second,
    ):
        state = await consume_sessions(
            [
                server_uri(first),
                server_uri(second),
            ]
        )

    assert state.valid
    assert state.last_sequence == 201
    assert state.invalidations == 1
    assert state.applied_updates == 2
