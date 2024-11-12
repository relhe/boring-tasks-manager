import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def send_email(recipient, subject, message):
    # Check if recipient and subject are provided
    if not recipient or not subject:
        print("Error: Recipient and subject are required.")
        return

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {recipient} successfully.")
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")


def schedule_daily_email(recipient, subject, message, send_time="08:00"):
    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == send_time:
            send_email(recipient, subject, message)
            time.sleep(60)  # Wait a minute before checking the time again


# Usage
recipient_email = ["abc@gmail.com", "def@yahoo.com"]
email_subject = "Daily Reminder"
email_message = "This is your daily reminder to check your tasks prepare your max!"

# Uncomment this line to run the reminder on schedule
# schedule_daily_email(recipient_email, email_subject, email_message)

# Or send an email directly
for recipient_email in recipient_email:
    send_email(recipient_email, email_subject, email_message)
