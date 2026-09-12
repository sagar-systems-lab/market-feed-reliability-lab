import json
from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class Snapshot:
    sequence: int


@dataclass(frozen=True, slots=True)
class Update:
    sequence: int


FeedMessage: TypeAlias = Snapshot | Update


def encode_message(message: FeedMessage) -> str:
    if isinstance(message, Snapshot):
        message_type = "snapshot"
    else:
        message_type = "update"

    return json.dumps(
        {
            "type": message_type,
            "sequence": message.sequence,
        },
        separators=(",", ":"),
    )


def decode_message(raw: str) -> FeedMessage:
    try:
        payload = json.loads(raw)
        message_type = payload["type"]
        sequence = payload["sequence"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError("invalid feed message") from exc

    if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
        raise ValueError("invalid sequence")

    if message_type == "snapshot":
        return Snapshot(sequence)

    if message_type == "update":
        return Update(sequence)

    raise ValueError(f"unknown message type: {message_type!r}")
