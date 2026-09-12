from market_feed_lab.orderbook import ApplyResult, FeedState


def test_snapshot_restores_invalid_state():
    state = FeedState()
    state.load_snapshot(200)

    assert state.apply_update(202) is ApplyResult.GAP
    assert not state.valid

    assert state.apply_update(203) is ApplyResult.INVALID_STATE

    state.load_snapshot(250)

    assert state.valid
    assert state.last_sequence == 250
    assert state.apply_update(251) is ApplyResult.APPLIED
