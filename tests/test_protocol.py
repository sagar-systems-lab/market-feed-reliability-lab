import pytest

from market_feed_lab.protocol import (
    Snapshot,
    Update,
    decode_message,
    encode_message,
)


@pytest.mark.parametrize(
    "message",
    [
        Snapshot(sequence=100),
        Update(sequence=101),
    ],
)
def test_message_round_trip(message):
    assert decode_message(encode_message(message)) == message


def test_unknown_message_type_is_rejected():
    with pytest.raises(ValueError, match="unknown message type"):
        decode_message('{"type":"heartbeat","sequence":10}')


def test_invalid_sequence_is_rejected():
    with pytest.raises(ValueError, match="invalid sequence"):
        decode_message('{"type":"update","sequence":-1}')
