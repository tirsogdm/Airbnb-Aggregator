import yaml
import logging
import imaplib
import email
from email.header import decode_header
import re
import json


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


# use of "status"
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
    decoded_fragments = decode_header(subject_header)
    subject = ''

    for fragment, encoding in decoded_fragments:
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


def split_body_and_forward(body):
    lines = body.splitlines()
    main_body, forwarded_content = list(), list()
    forwarding = False

    for line in lines:
        forwarding = "mensaje reenviado" in line.lower() or line.startswith(">")

        if forwarding:
            forwarded_content.append(line)
        else:
            main_body.append(line)

    return "\n".join(main_body).strip(), "\n".join(forwarded_content).strip()


def fetch_emails(mail, messages, sender_address, pattern):
    email_ids = messages[0].split()
    emails = list()

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        if status == "OK":
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # "subject" and "from" fields to match relevant emails
            subject = decode_subject(msg["Subject"])
            sender = msg["From"]

            if sender_address.lower() in sender.lower() and re.match(pattern, subject):
                body = get_email_content(msg)
                main_body, forwarded_content = split_body_and_forward(body)

                email_data = {
                    "date": msg["Date"],
                    "subject": subject,
                    "from": sender,
                    "to": msg["To"],
                    "cc": msg["Cc"],
                    "bcc": msg["Bcc"],
                    "main-body": main_body,
                    "forwarded-content": forwarded_content,
                    "content-type": msg.get_content_type(),
                }
                emails.append(email_data)

        else:
            print(f"Failed to fetch email ID {email_id}")

    return emails


def store_email_data(email_data, filename="email_data.json"):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(email_data, file, ensure_ascii=False, indent=4)
    print(f"Email data saved to {filename}")


def main():
    credentials = load_credentials('credentials.yaml')
    mail, messages = connect_to_gmail_imap(*credentials)
    pattern = r"^(CH7|V41): Hemos enviado un cobro de \d{1,3}(\.\d{3})*,\d{2}"
    sender_address = "madridrentalsmadrid@gmail.com"

    emails = fetch_emails(mail, messages, sender_address, pattern)
    print(f"Fetched {len(emails)} emails:\n{emails}")
    # store_email_data(emails)
    mail.close()
    mail.logout()


if __name__ == '__main__':
    main()
