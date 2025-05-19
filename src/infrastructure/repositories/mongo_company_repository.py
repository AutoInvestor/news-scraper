from typing import Optional, List

from pymongo import MongoClient

from src.domain.company import Company
from src.domain.company_repository import CompanyRepository
from src.logger import get_logger

logger = get_logger(__name__)


class MongoCompanyRepository(CompanyRepository):
    def __init__(self, uri: Optional[str], db_name: str):
        self._enabled = bool(uri)
        if not self._enabled:
            logger.warning(
                "No MONGODB_URI provided: MongoCompanyRepository disabled, using dummy behavior."
            )
            return

        client = MongoClient(uri)
        self._coll = client[db_name]["companies"]

    def exists_by_id(self, id_: str) -> bool:
        if not self._enabled:
            return False

        return self._coll.find_one({"_id": id_}) is not None

    def exists_by_ticker(self, ticker: str) -> bool:
        if not self._enabled:
            return False

        return self._coll.find_one({"ticker": ticker}) is not None

    def get_all(self) -> List[Company]:
        if not self._enabled:
            return []

        cursor = self._coll.find({}, {"_id": 1, "ticker": 1})
        companies: List[Company] = [
            Company(id=doc["_id"], ticker=doc["ticker"]) for doc in cursor
        ]
        return companies

    def find_by_ticker(self, ticker: str) -> Optional[Company]:
        if not self._enabled:
            return None

        doc = self._coll.find_one({"ticker": ticker}, {"_id": 1, "ticker": 1})
        if not doc:
            return None

        return Company(id=doc["_id"], ticker=doc["ticker"])

    def save(self, company: Company) -> None:
        if not self._enabled:
            return

        doc = {"_id": company.id, "ticker": company.ticker}

        self._coll.replace_one({"_id": company.id}, doc, upsert=True)
