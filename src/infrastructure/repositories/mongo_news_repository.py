from typing import Any, Dict, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from src.domain.news import News
from src.domain.news_repository import NewsRepository


class MongoNewsRepository(NewsRepository):
    def __init__(self, uri: Optional[str], db_name: str):
        self._enabled: bool = bool(uri)
        self._client: MongoClient = MongoClient(uri)
        self._coll: Collection = self._client[db_name]["news"]

    def exists_by_id(self, id_: str) -> bool:
        if not self._enabled:
            return False
        return self._coll.count_documents({"_id": id_}, limit=1) > 0

    def save(self, news: News) -> None:
        if not self._enabled:
            return

        doc: Dict[str, Any] = {
            "_id": news.id,
            "ticker": news.ticker,
            "title": news.title,
            "url": news.url,
            "date": news.date,
        }

        self._coll.update_one({"_id": news.id}, {"$set": doc}, upsert=True)
