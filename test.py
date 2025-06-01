from interface_adapters.gmail_reader import GmailReader
from dotenv import load_dotenv
import os

# Optional: load .env credentials (recommended)
load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
sender_address = os.getenv("SENDER_ADDRESS")
# subject_patterns = os.getenv("SBJ_PATTERNS").split(",")
subject_patterns = [r"^(CH7|V41):? Hemos enviado un cobro de \d{1,3}(\.\d{3})*,\d{2}", r"^(CH7|V41):? A \d{1,3}(\.\d{3})*,\d{2} € payout was sent"]

reader = GmailReader(username, password, sender_address, subject_patterns)

emails = reader.fetch_emails()

for i, email in enumerate(emails):
    print(f"\n--- EMAIL #{i+1} ---")
    print(email.get("date"))
    print(email.get("subject"))