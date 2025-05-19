from datetime import datetime, timezone
from typing import Dict, List, Optional

from src.domain.news import News
from src.domain.news_fetcher import NewsFetcher


class InMemoryNewsFetcher(NewsFetcher):
    _news: Dict[str, List[News]] = {
        "NFLX": [
            News.create(
                id_="NFLX-2025-05-17T14:30:00Z-1",
                ticker="NFLX",
                date=datetime(2025, 5, 17, 14, 30, tzinfo=timezone.utc),
                title="Netflix expands ad-supported tier to 20 new countries",
                url="https://example.com/netflix-ad-tier-expansion",
            ),
            News.create(
                id_="NFLX-2025-05-18T09:15:00Z-2",
                ticker="NFLX",
                date=datetime(2025, 5, 18, 9, 15, tzinfo=timezone.utc),
                title="Netflix shares surge after blockbuster Q1 earnings",
                url="https://example.com/netflix-q1-2025-earnings",
            ),
        ],
        "AAPL": [
            News.create(
                id_="AAPL-2025-05-16T08:00:00Z-1",
                ticker="AAPL",
                date=datetime(2025, 5, 16, 8, 0, tzinfo=timezone.utc),
                title="Apple unveils M4 Ultra chip at WWDC 25",
                url="https://example.com/apple-m4-ultra",
            ),
            News.create(
                id_="AAPL-2025-05-18T11:45:00Z-2",
                ticker="AAPL",
                date=datetime(2025, 5, 18, 11, 45, tzinfo=timezone.utc),
                title="Apple to offer generative-AI features in iOS 19",
                url="https://example.com/apple-ios19-ai",
            ),
        ],
    }

    def get_latest_news(self, ticker: str) -> Optional[News]:
        news_list = self._news.get(ticker.upper(), [])
        return news_list[-1] if news_list else None
