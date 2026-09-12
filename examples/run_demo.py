import asyncio

from websockets.asyncio.server import serve

from market_feed_lab.client import consume_feed, consume_sessions
from market_feed_lab.faults import drop_at, duplicate_at
from market_feed_lab.metrics import summarize
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


def print_summary(name, state):
    result = summarize(state)

    print(
        f"{name:<18} "
        f"valid={result.valid} "
        f"seq={result.last_sequence} "
        f"applied={result.applied_updates} "
        f"duplicates={result.duplicates} "
        f"invalidations={result.invalidations}"
    )


async def main():
    feed = [
        Snapshot(sequence=100),
        Update(sequence=101),
        Update(sequence=102),
        Update(sequence=103),
    ]

    print_summary("healthy", await consume(feed))
    print_summary("duplicate", await consume(duplicate_at(feed, 1)))
    print_summary("sequence gap", await consume(drop_at(feed, 2)))

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
        first_port = first.sockets[0].getsockname()[1]
        second_port = second.sockets[0].getsockname()[1]

        recovered = await consume_sessions(
            [
                f"ws://127.0.0.1:{first_port}",
                f"ws://127.0.0.1:{second_port}",
            ]
        )

    print_summary("reconnect", recovered)


if __name__ == "__main__":
    asyncio.run(main())
