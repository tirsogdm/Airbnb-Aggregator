import re
from PyQt5.QtCore import QDateTime


class Payment():
    def __init__(self, amount, reservations, raw):
        self.amount = self.formatAmount(amount)
        self.reservations = [Reservation(reservation)
                             for reservation in reservations]
        self.building = self.reservations[0].building
        self.raw = raw
        self.date = None
        self.published = False

    def formatAmount(self, number_str):
        number_str = number_str.replace('.', '')
        number_str = number_str.replace(',', '.')
        return float(number_str)

    def setDate(self, string_date):
        date_format = 'ddd, dd MMM yyyy HH:mm:ss'
        stripped_date = re.sub(r' \+\d{4}$', '', string_date)
        padded_date = re.sub(r'(\b\d\b) ', r'0\1 ', stripped_date)
        self.date = QDateTime.fromString(padded_date, date_format)

    def setRaw(self, raw):
        self.raw = raw

    def __repr__(self):
        return f'> {self.amount}€ payment - {len(self.reservations)} reservations'


class Reservation():
    def __init__(self, reservation):
        self.date_in = reservation[0]
        self.date_out = reservation[1]
        self.id = reservation[2]
        self.guest_name = reservation[3]
        self.apartment_desc = reservation[4]
        self.listing_id = reservation[5]
        self.amount = reservation[6]
        self.building = None
        self.apartment = None

        self.extract_building_apartment()

    def __repr__(self):
        pass

    def extract_building_apartment(self):
        if "a 3 calles de Gran Vía" in self.apartment_desc:
            self.building = "V41"
        elif "junto a la Gran Vía" in self.apartment_desc:
            self.building = "CH7"

        match = re.search(r'\b\w+\b$', self.apartment_desc)
        if match:
            code = match.group(0)

            if code.startswith("V"):
                code = code[1:]

            self.apartment = code
