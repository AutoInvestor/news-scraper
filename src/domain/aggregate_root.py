from typing import List

from src.domain.events import DomainEvent


class AggregateRoot:
    def __init__(self) -> None:
        self._events: List[DomainEvent] = []

    def _record_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def release_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
