from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from src.domain.aggregate_root import AggregateRoot
from src.domain.events import DomainEvent


def _news_created_event(news: "News") -> DomainEvent:
    return DomainEvent(
        event_id=str(uuid4()),
        occurred_at=datetime.now(timezone.utc).isoformat(),
        aggregate_id=news.id,
        version=1,
        type="NEW_LATEST_NEWS",
        payload={
            "ticker": news.ticker,
            "title": news.title,
            "url": news.url,
            "date": news.date.isoformat(),
        },
    )


class News(AggregateRoot):
    __slots__ = ("_id", "_ticker", "_date", "_title", "_url")

    _INIT_SENTINEL = object()

    def __init__(
        self,
        _sentinel: object,  # must be News._INIT_SENTINEL
        *,
        id: str,
        ticker: str,
        date: datetime,
        title: str,
        url: str,
    ) -> None:
        if _sentinel is not News._INIT_SENTINEL:
            raise RuntimeError("Use News.create() or News.create_empty().")

        super().__init__()

        self._id = id
        self._ticker = ticker
        self._date = date
        self._title = title
        self._url = url

    @classmethod
    def create(
        cls,
        *,
        ticker: str,
        title: str,
        url: str,
        date: datetime,
        id_: str,
    ) -> "News":
        instance = cls(
            cls._INIT_SENTINEL,
            id=id_,
            ticker=ticker,
            date=date or datetime.now(timezone.utc),
            title=title,
            url=url,
        )

        instance._record_event(_news_created_event(instance))

        return instance

    @property
    def id(self) -> str:
        return self._id

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, News):
            return False
        return self.ticker == other.ticker and self.title == other.title
