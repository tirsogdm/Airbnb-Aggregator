class ExtractPayment:
    """
    Extracts a payment from a email.
    """
    def __init__(self, email_reader, payment_parser):
        self.email_reader = email_reader # Interface to fetch emails
        self.payment_parser = payment_parser # Interface to parse emails for payments

    def execute(self):
        raw_emails = self.email_reader.fetch_emails()
        payments = []

        for email in raw_emails:
            payment = self.payment_parser.parse(email)
            if payment:
                payments.append(payment)

        return payments
