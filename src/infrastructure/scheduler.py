from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo


class Scheduler:
    def __init__(self, timezone: str = "Europe/Madrid"):
        self.__scheduler = AsyncIOScheduler(timezone=ZoneInfo(timezone))

    def add_minutely_job(self, coro):
        trigger = CronTrigger.from_crontab("* * * * *")
        self.__scheduler.add_job(coro, trigger, coalesce=True, misfire_grace_time=30)

    def start(self):
        self.__scheduler.start()

    def shutdown(self):
        self.__scheduler.shutdown()
