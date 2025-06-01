import re
from entities.amount import Amount

class Reservation():
    """
    Represents a reservation.
    """
    def __init__(self, date_in, date_out, id, guest_name, apartment_desc, listing_id, amount, building):
        self.date_in = date_in
        self.date_out = date_out
        self.id = id
        self.guest_name = guest_name
        self.apartment_desc = apartment_desc
        self.listing_id = listing_id
        self.amount = Amount(amount)
        self.building = building
        self.apartment = "None"

    def get_apartment(self):
        pass