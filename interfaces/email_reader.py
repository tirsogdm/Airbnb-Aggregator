from abc import ABC, abstractmethod
from typing import List

class EmailReader(ABC):
    @abstractmethod
    def fetch_emails(self) -> List[str]:
        """Returns raw email content (or structured email objects)."""
        pass