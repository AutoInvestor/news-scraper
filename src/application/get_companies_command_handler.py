from dataclasses import dataclass
from typing import List
from src.domain.company_repository import CompanyRepository
from src.logger import get_logger

logger = get_logger(__name__)


@dataclass
class CompaniesTicker:
    tickers: List[str]


class GetCompaniesCommandHandler:
    def __init__(self, repository: CompanyRepository):
        self.__repository = repository

    def handle(self) -> CompaniesTicker:
        companies = self.__repository.get_all()
        tickers = [company.ticker for company in companies]

        return CompaniesTicker(tickers)
