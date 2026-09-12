from market_feed_lab.orderbook import ApplyResult, FeedState


def test_duplicate_update_is_ignored():
    state = FeedState()
    state.load_snapshot(100)

    assert state.apply_update(101) is ApplyResult.APPLIED
    assert state.apply_update(101) is ApplyResult.DUPLICATE

    assert state.valid
    assert state.last_sequence == 101
    assert state.applied_updates == 1
    assert state.duplicates == 1
