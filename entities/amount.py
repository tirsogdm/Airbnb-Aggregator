
class Amount(float):
    """
    Represents an amount.
    """
    def __new__(cls, value):
        if isinstance(value, str):
            value = value.replace('.', '').replace(',', '.')
            value = float(value)
        return super().__new__(cls, value)

    def to_string(self):
        return f'{self.value} €'