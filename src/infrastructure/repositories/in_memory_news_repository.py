from typing import List

from src.domain.news import News
from src.domain.news_repository import NewsRepository


class InMemoryNewsRepository(NewsRepository):
    def __init__(self) -> None:
        self._items: List[News] = []

    def exists_by_id(self, id_: str) -> bool:
        return any(item.id == id_ for item in self._items)

    def save(self, news: News) -> None:
        for idx, stored in enumerate(self._items):
            if stored.id == news.id:
                self._items[idx] = news
                return
        self._items.append(news)
