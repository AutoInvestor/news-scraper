from typing import List

from src.application.get_companies_command_handler import GetCompaniesCommandHandler
from src.application.schedule_get_latest_news_command_handler import (
    ScheduleGetLatestNewsCommandHandler,
    ScheduleGetLatestNewsCommand,
)
from src.infrastructure.scheduler import Scheduler


class LatestNewsPoller:
    def __init__(
        self,
        scheduler: Scheduler,
        get_companies_handler: GetCompaniesCommandHandler,
        schedule_latest_news_handler: ScheduleGetLatestNewsCommandHandler,
    ):
        self.__scheduler = scheduler
        self.__get_companies_handler = get_companies_handler
        self.__schedule_latest_news_handler = schedule_latest_news_handler

    async def __job(self):
        tickers: List[str] = self.__get_companies_handler.handle().tickers
        for t in tickers:
            self.__schedule_latest_news_handler.handle(ScheduleGetLatestNewsCommand(t))

    def start(self):
        self.__scheduler.add_minutely_job(self.__job)

    def stop(self):
        self.__scheduler.shutdown()
