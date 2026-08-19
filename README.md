# Papa-Airbnb

Desktop PyQt5 tool used to fetch Airbnb payout emails from Gmail, extract reservation/payment data, and review/export monthly income.

## Features
- Fetches payout-related Airbnb emails from Gmail IMAP.
- Parses forwarded email content into structured payments and reservations.
- Displays payments with month/year filtering and search.
- Shows reservation details and raw forwarded message for each payment.
- Exports visible monthly data to an Excel file split by building (`CH7`, `V41`).

## Requirements
- Python 3.10+ (recommended)
- Gmail account access for IMAP

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the project root with:

```env
USERNAME=your_email@gmail.com
******
EMAIL_SENDER=express@airbnb.com
```

Notes:
- `PASSWORD` should be a Gmail app password (recommended), not your main account password.
- The app filters subjects for payout notifications matching `CH7`/`V41`.

## Run

```bash
python /home/runner/work/Papa-Airbnb/Papa-Airbnb/main.py
```

On startup, the app:
1. Reuses `email_data.json` if it was created in the last 15 minutes.
2. Otherwise fetches inbox emails and stores parsed raw data in `email_data.json`.
3. Loads payments into the UI for filtering, inspection, and export.

## Project Structure
- `main.py` – app entry point.
- `EmailFetchThread.py` – Gmail IMAP fetch + local JSON cache writer.
- `ExtractPayments.py` – regex parsing and payment extraction.
- `Representations.py` – payment/reservation/date/amount models.
- `GUI/` – main window, tables, filters, dialogs, and detail views.
- `assets/` – application assets (icon/logo).
