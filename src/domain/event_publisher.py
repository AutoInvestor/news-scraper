from abc import ABC, abstractmethod
from typing import List

from src.domain.events import DomainEvent


class DomainEventPublisher(ABC):
    @abstractmethod
    def publish(self, events: List[DomainEvent]): ...
