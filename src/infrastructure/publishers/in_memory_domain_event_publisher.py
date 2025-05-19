from typing import List

from src.domain.event_publisher import DomainEventPublisher
from src.domain.events import DomainEvent
from src.logger import get_logger

logger = get_logger(__name__)


class InMemoryDomainEventPublisher(DomainEventPublisher):
    def __init__(self):
        self.published_events: list[DomainEvent] = []
        logger.info("Initialized InMemoryDomainEventPublisher")

    def publish(self, events: List[DomainEvent]):
        for evt in events:
            self.published_events.append(evt)

            logger.info(
                "Published event %s for aggregate %s", evt.type, evt.aggregate_id
            )
