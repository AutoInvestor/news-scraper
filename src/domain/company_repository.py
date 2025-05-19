from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.company import Company


class CompanyRepository(ABC):
    @abstractmethod
    def exists_by_id(self, id_: str) -> bool: ...

    @abstractmethod
    def exists_by_ticker(self, ticker: str) -> bool: ...

    @abstractmethod
    def find_by_ticker(self, ticker: str) -> Optional[Company]: ...

    @abstractmethod
    def get_all(self) -> List[Company]: ...

    @abstractmethod
    def save(self, company: Company) -> None: ...
