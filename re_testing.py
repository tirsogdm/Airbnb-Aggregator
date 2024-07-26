import re

# Regular expression to match numbers between 0,00 and 10.000,00
pattern = r"^(CH7|V41): Hemos enviado un cobro de ((\d{1,3}(\.\d{3})*|\d{1,2}(\.\d{3})*)?,\d{2}|10\.000,00) €$"

# Test subjects
subjects = [
    "CH7: Hemos enviado un cobro de 0,00 €",
    "CH7: Hemos enviado un cobro de 9,99 €",
    "CH7: Hemos enviado un cobro de 10,00 €",
    "CH7: Hemos enviado un cobro de 999,99 €",
    "CH7: Hemos enviado un cobro de 1.000,00 €",
    "CH7: Hemos enviado un cobro de 10.000,00 €",
    "V41: Hemos enviado un cobro de 3.000,11 €",
    "V41: Hemos enviado un cobro de 1.009,21 €",
    "CH7: Hemos enviado un cobro de 421,71 €",
    "V41: Hemos enviado un cobro de 12,34 €",
    "CH7: Hemos enviado un cobro de 123,45 €",
    "CH7: Hemos enviado un cobro de 10.000,01 €"  # Should not match
]

for subject in subjects:
    if re.match(pattern, subject):
        print(f"Matched: {subject}")
    else:
        print(f"Did not match: {subject}")
