from abc import ABC, abstractmethod
from typing import Optional
from src.domain.news import News


class NewsFetcher(ABC):
    @abstractmethod
    def get_latest_news(self, ticker: str) -> Optional[News]: ...
