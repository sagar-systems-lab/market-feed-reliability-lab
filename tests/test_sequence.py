from market_feed_lab.orderbook import ApplyResult, FeedState


def test_contiguous_updates_are_accepted():
    state = FeedState()
    state.load_snapshot(100)

    assert state.apply_update(101) is ApplyResult.APPLIED
    assert state.apply_update(102) is ApplyResult.APPLIED

    assert state.valid
    assert state.last_sequence == 102
    assert state.applied_updates == 2


def test_gap_invalidates_local_state():
    state = FeedState()
    state.load_snapshot(100)

    assert state.apply_update(102) is ApplyResult.GAP

    assert not state.valid
    assert state.invalidations == 1