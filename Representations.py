import re
from enum import Enum
from PyQt5.QtCore import QDateTime


# --------------------------
# --------- Payment --------
# --------------------------
class Payment():
    def __init__(self, amount, reservations, date_string, raw):
        self.num_reservations = len(reservations)
        self.reservations = list()
        self.building = 'undef'
        self.raw = raw
        self.datetime = CDateTime(
            date_string, DateTimeFormat.datetime, self.preprocess_date_string)

        if self.num_reservations > 0:
            self.reservations = [Reservation(reservation) for reservation in reservations]
            self.building = self.reservations[0].building
        else:
            print(self.datetime.toString())

        if amount:
            self.amount = Amount(amount)
        else:
            self.amount = Amount(0.0)
            print(self.datetime.toString())


        """
        self.date_time = self.format_str_datetime(
            self.process_date_string(date_string))
        self.date = self.date_time.date()
        """

    def preprocess_date_string(self, string_date):
        stripped_date = re.sub(r' \+\d{4}$', '', string_date)
        padded_date = re.sub(r'(\b\d\b) ', r'0\1 ', stripped_date)
        return padded_date

    def __repr__(self):
        return f'> {self.amount}€ payment - {len(self.reservations)} reservations'


# --------------------------
# ------- Reservation ------
# --------------------------
class Reservation():
    def __init__(self, reservation):
        self.date_in = CDateTime(reservation[0], DateTimeFormat.us_date)
        self.date_out = CDateTime(reservation[1], DateTimeFormat.us_date)

        self.id = reservation[2]
        self.guest_name = reservation[3]
        self.apartment_desc = reservation[4]
        self.listing_id = reservation[5]
        self.amount = Amount(reservation[6])
        self.building = None
        self.apartment = None

        self.extract_building_apartment()

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
            elif code == "Madrid":
                code = "Ático"

            self.apartment = code


# --------------------------
# -------- DateTime --------
# --------------------------
class CDateTime(QDateTime):
    def __init__(self, date_string, type, preprocesor=None):
        if preprocesor:
            date_string = preprocesor(date_string)

        dt = QDateTime.fromString(date_string, type.value)

        super().__init__(dt)

    def toString(self):
        return super().toString(DateTimeFormat.eur_date.value)


class DateTimeFormat(Enum):
    eur_date = "dd/MM/yyyy"
    us_date = "MM/dd/yyyy"
    datetime = "ddd, dd MMM yyyy HH:mm:ss"


# --------------------------
# --------- Amount ---------
# --------------------------
class Amount(float):
    def __new__(cls, value):
        if isinstance(value, str):
            value = value.replace('.', '')
            value = value.replace(',', '.')
            value = float(value)

        return super().__new__(cls, value)

    def __init__(self, value):
        self.value = value

    def toString(self):
        return f'{self.value} €'


# --------------------------
# --------- TESTING --------
# --------------------------
if __name__ == "__main__":
    print("-------")

    custom_dt = CDateTime(
        "Tue, 23 Jul 2024 14:00:00", DateTimeFormat.datetime)
    print(custom_dt)
    print(custom_dt.date())
    print(custom_dt.time())
    print(custom_dt.toString())

    print("-------")

    eur = Amount(1932.123)
    print(eur)
    print(eur.toString())
