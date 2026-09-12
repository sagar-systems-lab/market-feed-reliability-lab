from enum import Enum


class ApplyResult(Enum):
    APPLIED = "applied"
    DUPLICATE = "duplicate"
    GAP = "gap"
    OUT_OF_ORDER = "out_of_order"
    INVALID_STATE = "invalid_state"


class FeedState:
    def __init__(self) -> None:
        self.last_sequence: int | None = None
        self.valid = False
        self.applied_updates = 0
        self.duplicates = 0
        self.invalidations = 0

    def load_snapshot(self, sequence: int) -> None:
        self.last_sequence = sequence
        self.valid = True

    def invalidate(self) -> None:
        if self.valid:
            self.valid = False
            self.invalidations += 1

    def apply_update(self, sequence: int) -> ApplyResult:
        if not self.valid or self.last_sequence is None:
            return ApplyResult.INVALID_STATE

        if sequence == self.last_sequence:
            self.duplicates += 1
            return ApplyResult.DUPLICATE

        expected = self.last_sequence + 1

        if sequence > expected:
            self.valid = False
            self.invalidations += 1
            return ApplyResult.GAP

        if sequence < expected:
            self.valid = False
            self.invalidations += 1
            return ApplyResult.OUT_OF_ORDER

        self.last_sequence = sequence
        self.applied_updates += 1
        return ApplyResult.APPLIED
