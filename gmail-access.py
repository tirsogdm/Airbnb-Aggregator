import yaml
import logging
import imaplib
import pandas as pd
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


def connect_to_gmail_imap(user, password):
    imap_url = 'imap.gmail.com'
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, password)
        mail.search('inbox')
        return mail
    except Exception as e:
        logging.error(f"Connection failed {e}")
        raise


def get_emails_to_print(mail, filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        emails_to_print = data['emails']

    summary = pd.DataFrame(columns=['Emails', 'Count'])
    for email in emails_to_print:
        _, messages = mail.search(None, f'FROM "{email}"')
        # mail.store(messages, '+FLAGS', '\\Deleted')
        summary = summary.append(
            {'Email': email, 'Count': len(messages)}, ignore_index=True)
    return summary


def main():
    credentials = load_credentials('credentials.yaml')
    mail = connect_to_gmail_imap(*credentials)
    summary = get_emails_to_print(mail, 'email_list.json')
    print(summary)


if __name__ == '__main__':
    main()
