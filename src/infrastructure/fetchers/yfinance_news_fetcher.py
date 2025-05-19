import uuid
from datetime import datetime, timezone
from typing import Optional, List

import yfinance as yf

from src.domain.news import News
from src.domain.news_fetcher import NewsFetcher
from src.logger import get_logger

logger = get_logger(__name__)


class YFinanceNewsFetcher(NewsFetcher):
    def make_deterministic_id(
        self, ticker: str, pub_datetime: datetime, title: str, url: str
    ) -> str:
        """Create a stable UUIDv5 so the same article always maps to the same ID."""
        raw = "||".join(
            [
                ticker.upper().strip(),
                pub_datetime.isoformat(),
                title.strip(),
                url.strip(),
            ]
        )
        return str(uuid.uuid5(uuid.NAMESPACE_URL, raw))

    # ---------------------------------------------------------------

    def get_latest_news(self, ticker: str) -> Optional[News]:
        ticker_upper = ticker.upper()
        logger.debug("[YF] Fetching news for %s", ticker_upper)

        stock = yf.Ticker(ticker_upper)
        news_list: List[dict] = stock.news or []
        if not news_list:
            logger.info("[YF] No news entries returned for %s", ticker_upper)
            return None

        news_objects: List[News] = []
        for item in news_list:
            content = item.get("content", {})

            # --- Parse publication datetime -------------------------
            pub_date_str = content.get("pubDate")
            if not pub_date_str:
                logger.debug("[YF] Skipping item without pubDate for %s", ticker_upper)
                continue
            try:
                pub_datetime = datetime.strptime(
                    pub_date_str, "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc)
            except ValueError:
                logger.warning(
                    "[YF] Could not parse pubDate '%s' for %s",
                    pub_date_str,
                    ticker_upper,
                )
                continue

            # --- Extract title & URL --------------------------------
            title = content.get("title", "").strip()
            url = (
                content.get("previewUrl")
                or content.get("canonicalUrl", {}).get("url", "")
            ).strip()
            if not url:
                logger.debug("[YF] Skipping item without URL for %s", ticker_upper)
                continue

            # --- Build News aggregate -------------------------------
            news_objects.append(
                News.create(
                    id_=self.make_deterministic_id(
                        ticker_upper, pub_datetime, title, url
                    ),
                    ticker=ticker_upper,
                    date=pub_datetime,
                    title=title,
                    url=url,
                )
            )

        if not news_objects:
            logger.info("[YF] After filtering, no usable news for %s", ticker_upper)
            return None

        latest_news = max(news_objects, key=lambda n: n.date)
        logger.debug("[YF] Latest news for %s is %s", ticker_upper, latest_news.id)
        return latest_news
