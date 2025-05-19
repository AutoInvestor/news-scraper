import uvicorn
from fastapi import FastAPI

from src.application.get_companies_command_handler import GetCompaniesCommandHandler
from src.application.register_company_command_handler import (
    RegisterCompanyCommandHandler,
)
from src.application.schedule_get_latest_news_command_handler import (
    ScheduleGetLatestNewsCommandHandler,
)
from src.config import settings
from src.infrastructure.fetchers.in_memory_news_fetcher import InMemoryNewsFetcher
from src.infrastructure.fetchers.yfinance_news_fetcher import YFinanceNewsFetcher
from src.infrastructure.latest_news_poller import LatestNewsPoller
from src.infrastructure.listeners.pubsub_event_subscriber import PubSubEventSubscriber
from src.infrastructure.publishers.in_memory_domain_event_publisher import (
    InMemoryDomainEventPublisher,
)
from src.infrastructure.publishers.pubsub_event_publisher import PubSubEventPublisher
from src.infrastructure.repositories.in_memory_company_repository import (
    InMemoryCompanyRepository,
)
from src.infrastructure.repositories.in_memory_news_repository import (
    InMemoryNewsRepository,
)
from src.infrastructure.repositories.mongo_company_repository import (
    MongoCompanyRepository,
)
from src.infrastructure.repositories.mongo_news_repository import MongoNewsRepository
from src.infrastructure.scheduler import Scheduler
from src.logger import get_logger
from src.infrastructure.http_exception_handler import HttpExceptionHandler


app = FastAPI()
logger = get_logger(__name__)
logger.info("Starting up in %s mode", settings.ENVIRONMENT)

HttpExceptionHandler(app)

if settings.ENVIRONMENT.lower() == "testing":
    news_fetcher = InMemoryNewsFetcher()
    news_repo = InMemoryNewsRepository()
    company_repo = InMemoryCompanyRepository()
    publisher = InMemoryDomainEventPublisher()
else:
    news_fetcher = YFinanceNewsFetcher()
    news_repo = MongoNewsRepository(
        settings.MONGODB_URI.get_secret_value(), settings.MONGODB_DB
    )
    company_repo = MongoCompanyRepository(
        settings.MONGODB_URI.get_secret_value(), settings.MONGODB_DB
    )
    publisher = PubSubEventPublisher(settings.GCP_PROJECT, settings.PUBSUB_TOPIC)

# Pub/Sub subscriber wiring (only in production)
if settings.ENVIRONMENT.lower() != "testing":
    register_handler = RegisterCompanyCommandHandler(company_repo)
    subscriber = PubSubEventSubscriber(
        command_handler=register_handler,
        project_id=settings.GCP_PROJECT,
        subscription=settings.PUBSUB_SUBSCRIPTION_CORE,
    )

    @app.on_event("startup")
    def start_subscriber():
        subscriber.listen()

    @app.on_event("shutdown")
    def stop_subscriber():
        subscriber.stop()


# Wire the scheduler
scheduler = Scheduler()
poller = LatestNewsPoller(
    scheduler=scheduler,
    get_companies_handler=GetCompaniesCommandHandler(company_repo),
    schedule_latest_news_handler=ScheduleGetLatestNewsCommandHandler(
        news_fetcher, news_repo, company_repo, publisher
    ),
)


@app.on_event("startup")
async def _startup():
    poller.start()
    scheduler.start()


@app.on_event("shutdown")
async def _shutdown():
    poller.stop()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
