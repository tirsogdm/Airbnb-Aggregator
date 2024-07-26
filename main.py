import yaml
import logging
import imaplib
import email
from email.header import decode_header
import re


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


def decode_subject(subject_header):
    decoded_fragment = decode_header(subject_header)
    subject = ''

    for fragment, encoding in decoded_fragment:
        if isinstance(fragment, bytes):
            fragment = fragment.decode(encoding if encoding else "utf-8")
        subject += fragment

    return subject


def get_email_content(msg):
    if msg.is_multipart():
        for part in msg.walk():
            try:
                body = part.get_payload(decode=True).decode()
                return body
            except:
                pass

    else:
        try:
            body = msg.get_payload(decode=True).decode()
            return body
        except:
            pass

    return None


def fetch_print_subject(mail, messages, sender_address, re_pattern):
    email_ids = messages[0].split()
    count = 0

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        if status == "OK":
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Decode email subject
            subject = decode_subject(msg["Subject"])

            # Extract date
            date = msg["Date"]

            # Email sender
            sender = msg["From"]

            if sender_address.lower() in sender.lower():
                count += 1

                if re.match(re_pattern, subject.strip()):
                    print(f"Matched: |{subject}|")
                else:
                    print(f"Did not match: |{subject}|")

                body = get_email_content(msg)

                print(f"Date: {date}, From: {sender}, Subject:", subject)
                print("Content:")
                print(body)
                print("=" * 50)

        else:
            print(f"Failed to fetch email ID {email_id}")

    print(f"{count} emails found.")


def main():
    credentials = load_credentials('credentials.yaml')
    mail, messages = connect_to_gmail_imap(*credentials)
    # re_pattern = r"^(CH7|V41): Hemos enviado un cobro de \d{1,3}(\.\d{3})*,\d{2} €$"
    re_pattern = r"^(CH7|V41): Hemos enviado un cobro de \d{1,3}(?:\.\d{3})*,\d{2} €$"
    r_pattern = r"^(CH7|V41): Hemos enviado un cobro de ((\d{1,3}(\.\d{3})*|\d{1,2}(\.\d{3})*)?,\d{2}|10\.000,00) €$"

    sender_address = "madridrentalsmadrid@gmail.com"
    fetch_print_subject(mail, messages, sender_address, r_pattern)
    mail.close()
    mail.logout()


if __name__ == '__main__':
    main()
