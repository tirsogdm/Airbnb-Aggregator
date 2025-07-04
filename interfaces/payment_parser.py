from abc import ABC, abstractmethod
from typing import Optional
from entities.payment import Payment

class PaymentParser(ABC):
    @abstractmethod
    def parse(self, email_data: dict) -> Optional[Payment]:
        """Parses a single email's data into a Payment entity, or returns None if parsing fails."""
        pass