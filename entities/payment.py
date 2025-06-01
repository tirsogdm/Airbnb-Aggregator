from datetime import datetime

from entities.amount import Amount
from entities.reservation import Reservation

class Payment():
    """
    Represents a processed payment.
    """
    def __init__(self, amount, reservations, datetime: datetime, building: str, raw: str):
        self.datetime = datetime
        self.raw = raw
        self.building = building
        self.reservations = [Reservation(res, building) for res in reservations] if reservations else []
        self.num_reservations = len(self.reservations)

        self.amount = Amount(amount) if amount else Amount(0.0)

    def __repr__(self):
        return f'> {self.amount}€ payment - {self.num_reservations} reservations'