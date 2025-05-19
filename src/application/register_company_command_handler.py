from dataclasses import dataclass

from src.domain.company import Company
from src.domain.company_repository import CompanyRepository
from src.logger import get_logger

logger = get_logger(__name__)


@dataclass
class RegisterCompanyCommand:
    id: str
    ticker: str


class RegisterCompanyCommandHandler:
    def __init__(self, repository: CompanyRepository):
        self.__repository = repository

    def handle(self, command: RegisterCompanyCommand):
        if self.__repository.exists_by_id(command.id):
            return

        company = Company(command.id, command.ticker)
        self.__repository.save(company)
