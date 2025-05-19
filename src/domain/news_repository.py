from abc import ABC, abstractmethod

from src.domain.news import News


class NewsRepository(ABC):
    @abstractmethod
    def exists_by_id(self, id_: str) -> bool: ...

    @abstractmethod
    def save(self, news: News) -> None: ...
