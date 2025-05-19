import json
from typing import List

from google.cloud import pubsub_v1
from src.domain.event_publisher import DomainEventPublisher
from src.domain.events import DomainEvent
from src.logger import get_logger

logger = get_logger(__name__)


class PubSubEventPublisher(DomainEventPublisher):
    def __init__(self, project_id: str, topic: str):
        self._enabled = bool(project_id and topic)
        if not self._enabled:
            return

        self._publisher = pubsub_v1.PublisherClient()
        self._topic_path = self._publisher.topic_path(project_id, topic)

    def publish(self, events: List[DomainEvent]):
        if not self._enabled:
            return

        for event in events:
            message = json.dumps(
                {
                    "eventId": event.event_id,
                    "occurredAt": event.occurred_at,
                    "aggregateId": event.aggregate_id,
                    "version": event.version,
                    "type": event.type,
                    "payload": event.payload,
                }
            ).encode("utf-8")

            future = self._publisher.publish(self._topic_path, message, type=event.type)
            future.result()

            logger.info(
                "Published event %s for aggregate %s", event.type, event.aggregate_id
            )
