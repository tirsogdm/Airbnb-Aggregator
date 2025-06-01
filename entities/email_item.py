from datetime import datetime

class EmailItem:
    """
    Represents an email item.
    """
    def __init__(self, subject: str, sender: str, body: str, date: datetime):
        self.subject = subject
        self.sender = sender
        self.body = body
        self.date = date

    def is_payment(self) -> bool:
        """Filtering logic for payment emails."""
        return "payment" in self.subject.lower()