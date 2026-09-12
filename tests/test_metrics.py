from market_feed_lab.metrics import summarize
from market_feed_lab.orderbook import FeedState


def test_summary_reflects_feed_state():
    state = FeedState()
    state.load_snapshot(100)
    state.apply_update(101)
    state.apply_update(101)

    summary = summarize(state)

    assert summary.valid
    assert summary.last_sequence == 101
    assert summary.applied_updates == 1
    assert summary.duplicates == 1
    assert summary.invalidations == 0
