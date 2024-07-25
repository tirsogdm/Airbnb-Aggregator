import imaplib
import email
from email.header import decode_header


def fetch_and_print(all_email_ids, limit):
    email_ids = all_email_ids[-limit]
    for (count, email_id) in enumerate(email_ids, 1):
        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        if status == "OK":
            # Get the email content
            msg = email.message_from_bytes(msg_data[0][1])

            # Decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            # Print the email subject
            print(f"{count}. Subject:", subject)

        else:
            print(f"Failed to fetch email ID {email_id}")


def connect_and_auth(imap_server, email_user, email_pass):
    # Connect to server
    mail = imaplib.IMAP4_SSL(imap_server)
    print("Connected to server")

    # Login
    mail.login(email_user, email_pass)
    print("Logged in as", email_user)

    # Select mailbox
    status, messages = mail.select("inbox")

    if status != "OK":
        print("Failed to select mailbox. Status:", status)
        raise Exception("Failed to select mailbox")

    print("Mailbox selected")

    return mail


# Gmail IMAP server address
imap_server = "imap.gmail.com"
email_user = "gestioncasalaffitte@gmail.com"
email_pass = "ikofIscvbjzncsjy"

try:
    # Connect to server
    mail = imaplib.IMAP4_SSL(imap_server)
    print("Connected to server")

    # Login
    mail.login(email_user, email_pass)
    print("Logged in as", email_user)

    # Select mailbox
    status, messages = mail.select("inbox")

    if status != "OK":
        print("Failed to select mailbox. Status:", status)
        raise Exception("Failed to select mailbox")

    print("Mailbox selected")

    # Search all emails
    status, messages = mail.search(None, "ALL")

    if status == "OK":
        print("Emails found")
        # Convert to IDs
        email_ids = messages[0].split()

        # Call fetch and print
        fetch_and_print(email_ids, 10)

    else:
        print("Failed to search emails.")

except imaplib.IMAP4.error as e:
    print(f"IMAP error: {e}")

except Exception as e:
    print(f"An error occurred: {e}")


mail.close()
mail.logout()
