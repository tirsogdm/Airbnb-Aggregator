import yaml
import logging
import imaplib
import email
from email.header import decode_header


def load_credentials(filepath):
    try:
        with open(filepath, 'r') as file:
            credentials = yaml.safe_load(file)
            user = credentials['user']
            password = credentials['password']
            return user, password
    except Exception as e:
        logging.error(f"Failed to load credentials: {e}")
        raise


def connect_to_gmail_imap(user, password):
    imap_url = 'imap.gmail.com'
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, password)
        mail.select('inbox')
        status, messages = mail.search(None, 'ALL')
        return mail, messages

    except Exception as e:
        logging.error(f"Connection failed {e}")
        raise


def fetch_print(mail, messages):
    email_ids = messages[0].split()[-10]
    for (count, email_id) in enumerate(email_ids, 1):
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        if status == "OK":
            msg = email.message_from_bytes(msg_data[0][1])

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            print(f"{count}. Subject:", subject)

        else:
            print(f"Failed to fetch email ID {email_id}")


def main():
    credentials = load_credentials('credentials.yaml')
    print(*credentials)
    mail, messages = connect_to_gmail_imap(*credentials)
    fetch_print(mail, messages)
    mail.close()
    mail.logout()


if __name__ == '__main__':
    main()
