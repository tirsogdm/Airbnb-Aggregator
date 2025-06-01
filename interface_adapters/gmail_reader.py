from typing import List
import imaplib
import logging
import email
import re
from interfaces.email_reader import EmailReader

from email.header import decode_header

class GmailReader(EmailReader):
    """
    Reads emails from Gmail.
    """
    def __init__(self, username: str, password: str, sender_address: str, subject_patterns: List[str]):
        self.username = username
        self.password = password
        self.server = 'imap.gmail.com'
        self.sender_address = sender_address
        self.subject_patterns = [re.compile(p, re.IGNORECASE) for p in subject_patterns]

    def connect_to_imap(self):
        try:
            mail = imaplib.IMAP4_SSL(self.server)
            mail.login(self.username, self.password)
            mail.select('inbox')

            _, messages = mail.search(None, 'ALL')
            return mail, messages
        
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            raise

    def decode_subject(self, subject_header):
        decoded, encoding = decode_header(subject_header)[0]
        if isinstance(decoded, bytes):
            return decoded.decode(encoding or "utf-8", errors="ignore")
        return decoded

    def get_email_content(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_dispo = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_dispo:
                    try:
                        return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                    except:
                        continue  
        else:
            try:
                return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")
            except:
                pass
        return ""

    def split_body_and_fwd(self, body:str):
        lines = body.splitlines()
        main, fwd = [], []
        forwarding = False

        for line in lines:
            forwarding = "mensaje reenviado" in line.lower() or line.startswith(">")
            if forwarding:
                fwd.append(line)
            else:
                main.append(line)

        return "\n".join(main).strip(), "\n".join(fwd).strip()

    def fetch_emails(self):
        mail, messages = self.connect_to_imap()

        email_ids = messages[0].split()
        emails = []
        for eid in email_ids:
            status, msg_data = mail.fetch(eid, "(RFC822)")
            if status != 'OK':
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = self.decode_subject(msg["Subject"] or "")
            sender = msg["From"] or ""

            if self.sender_address.lower() not in sender.lower():
                continue

            if not any(p.match(subject) for p in self.subject_patterns):
                continue

            body = self.get_email_content(msg)
            main, fwd = self.split_body_and_fwd(body)

            email_data = {
                "date": msg["Date"],
                "subject": subject,
                "from": sender,
                "to": msg.get("To", ""),
                "cc": msg.get("Cc", ""),
                "bcc": msg.get("Bcc", ""),
                "main-body": main,
                "forwarded-content": fwd,
                "content-type": msg.get_content_type(),
            }
            emails.append(email_data)

        mail.close()
        mail.logout()
        return emails

if __name__ == "__main__":
    reader = GmailReader()