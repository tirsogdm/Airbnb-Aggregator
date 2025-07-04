from datetime import datetime
from typing import Optional
import re

from interfaces.payment_parser import PaymentParser
from entities.payment import Payment
from entities.amount import Amount
from entities.reservation import Reservation

class AirbnbPaymentParser(PaymentParser):
    def parse(self, email_data: dict) -> Optional[Payment]:
        """
        Parses Airbnb payment emails.
        """
        body = email_data.get("main-body", "")