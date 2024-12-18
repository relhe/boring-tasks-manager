########################################################################################################################
# Automated Email Sender and Scheduler Script                                                                          #
#                                                                                                                      #
# This script allows sending emails and scheduling daily email reminders using SMTP credentials loaded from .env file. #
# It supports bulk email sending and periodic scheduling for reminders.                                                #
#                                                                                                                      #
# Author: Renel Lherisson                                                                                              #
# Date: 2024-12-17                                                                                                     #
# Purpose: Automate email reminders and notifications.                                                                 #
# Dependencies:                                                                                                        #
#    - smtplib: Python's standard library for SMTP connections                                                         #
#    - dotenv: `pip install python-dotenv` for environment variables                                                   #
#    - email: For MIME message creation                                                                                #
########################################################################################################################

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class EmailScheduler:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))

    def send_email(self, recipient, subject, message, attachment_path=None):
        """
        Sends an email to a specified recipient, optionally attaching a file.

        Parameters:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        message (str): The body content of the email.
        attachment_path (str): The file path of the attachment (optional).

        Returns:
        None
        """
        if not recipient or not subject:
            print("Error: Recipient and subject are required.")
            return

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Attach a file if provided
        if attachment_path:
            try:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachment_path)}'
                )
                msg.attach(part)
            except Exception as e:
                print(f"Error attaching file: {e}")
                return

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.email_password)
            server.send_message(msg)
            server.quit()
            print(f"Email sent to {recipient} successfully.")
        except Exception as e:
            print(f"Error sending email to {recipient}: {e}")

    def schedule_daily_email(self, recipient, subject, message, send_time="08:00", attachment_path=None):
        """
        Schedules a daily email to be sent at a specific time, optionally with an attachment.

        Parameters:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        message (str): The body content of the email.
        send_time (str): The time in 24-hour format (default is "08:00").
        attachment_path (str): The file path of the attachment (optional).

        Returns:
        None
        """
        print(f"Scheduling daily email to {recipient} at {send_time}...")
        while True:
            current_time = datetime.now().strftime("%H:%M")
            if current_time == send_time:
                self.send_email(recipient, subject, message, attachment_path)
                time.sleep(60)


if __name__ == "__main__":
    email_scheduler = EmailScheduler()

    recipients = ["abc@gmail.com", "def@yahoo.com"]
    email_subject = "Daily Reminder"
    email_message = "This is your daily reminder to check your tasks and prepare your max!"
    # Replace with the actual path to your file
    attachment = "path/to/your/file.pdf"

    # Send emails directly
    for recipient in recipients:
        email_scheduler.send_email(
            recipient, email_subject, email_message, attachment)

    # Uncomment to schedule daily emails
    # email_scheduler.schedule_daily_email(recipients[0], email_subject, email_message, attachment_path=attachment)
