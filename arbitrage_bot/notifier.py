import smtplib
from email.mime.text import MIMEText
from config import EXCHANGES

class Notifier:
    def __init__(self):
        self.email = EXCHANGES['email']['api_key']  # Assuming email settings are in config

    def send_email(self, subject, message):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = self.email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.email, EXCHANGES['email']['api_secret'])
            server.send_message(msg)
