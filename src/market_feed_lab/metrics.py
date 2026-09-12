from dataclasses import dataclass

from market_feed_lab.orderbook import FeedState


@dataclass(frozen=True, slots=True)
class FeedSummary:
    valid: bool
    last_sequence: int | None
    applied_updates: int
    duplicates: int
    invalidations: int


def summarize(state: FeedState) -> FeedSummary:
    return FeedSummary(
        valid=state.valid,
        last_sequence=state.last_sequence,
        applied_updates=state.applied_updates,
        duplicates=state.duplicates,
        invalidations=state.invalidations,
    )
