from collections.abc import Sequence

from market_feed_lab.protocol import FeedMessage


def duplicate_at(
    messages: Sequence[FeedMessage],
    index: int,
) -> list[FeedMessage]:
    result = list(messages)
    result.insert(index + 1, result[index])
    return result


def drop_at(
    messages: Sequence[FeedMessage],
    index: int,
) -> list[FeedMessage]:
    result = list(messages)
    del result[index]
    return result


def swap_adjacent(
    messages: Sequence[FeedMessage],
    index: int,
) -> list[FeedMessage]:
    result = list(messages)
    result[index], result[index + 1] = result[index + 1], result[index]
    return result
