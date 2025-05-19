from dataclasses import dataclass
from typing import Optional

from src.domain.company_repository import CompanyRepository
from src.domain.news import News
from src.domain.news_fetcher import NewsFetcher
from src.domain.event_publisher import DomainEventPublisher
from src.domain.news_repository import NewsRepository
from src.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ScheduleGetLatestNewsCommand:
    ticker: str


class ScheduleGetLatestNewsCommandHandler:
    def __init__(
        self,
        news_fetcher: NewsFetcher,
        news_repository: NewsRepository,
        company_repository: CompanyRepository,
        event_publisher: DomainEventPublisher,
    ):
        self.__news_fetcher = news_fetcher
        self.__news_repository = news_repository
        self.__company_repository = company_repository
        self.__event_publisher = event_publisher

    def handle(self, command: ScheduleGetLatestNewsCommand):
        ticker = command.ticker

        if not self.__company_repository.exists_by_ticker(ticker):
            logger.warning(
                "[GetLatestNews] Company '%s' not registered – abort", ticker
            )
            return

        news: Optional[News] = self.__news_fetcher.get_latest_news(ticker)
        if news is None:
            logger.warning(
                "[GetLatestNews] No news returned by fetcher for '%s' – nothing to do",
                ticker,
            )
            return

        if self.__news_repository.exists_by_id(news.id):
            logger.debug(
                "[GetLatestNews] News item %s already in repository – ignoring duplicate",
                news.id,
            )
            return

        self.__news_repository.save(news)
        self.__event_publisher.publish(news.release_events())
