from typing import List, Optional

from src.domain.company import Company
from src.domain.company_repository import CompanyRepository


class InMemoryCompanyRepository(CompanyRepository):
    def __init__(self):
        self.__companies: List[Company] = [
            Company(id="AAPL", ticker="AAPL"),
            Company(id="MSFT", ticker="MSFT"),
            Company(id="AMZN", ticker="AMZN"),
            Company(id="GOOGL", ticker="GOOGL"),
            Company(id="NVDA", ticker="NVDA"),
            Company(id="TSLA", ticker="TSLA"),
            Company(id="NFLX", ticker="NFLX"),
            Company(id="ADBE", ticker="ADBE"),
            Company(id="INTC", ticker="INTC"),
        ]

    def exists_by_id(self, id_: str) -> bool:
        return any(c.id == id_ for c in self.__companies)

    def exists_by_ticker(self, ticker: str) -> bool:
        return any(c.ticker == ticker for c in self.__companies)

    def find_by_ticker(self, ticker: str) -> Optional[Company]:
        for c in self.__companies:
            if c.ticker == ticker:
                return c
        return None

    def get_all(self) -> List[Company]:
        return self.__companies

    def save(self, company: Company) -> None:
        for idx, stored in enumerate(self.__companies):
            if stored.ticker == company.ticker:
                self.__companies[idx] = company
                return

        self.__companies.append(company)
