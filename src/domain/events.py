from dataclasses import dataclass


@dataclass
class DomainEvent:
    event_id: str
    occurred_at: str
    aggregate_id: str
    version: int
    type: str
    payload: dict
