import os
from twilio.rest import Client
from datetime import datetime
import time
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_text_message(to_number, message):
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"Message sent to {to_number} successfully.")
    except Exception as e:
        print(f"Error sending message to {to_number}: {e}")

# Schedule daily SMS reminders (e.g., every day at 8 am)


def schedule_daily_text(to_number, message, send_time="08:00"):
    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == send_time:
            send_text_message(to_number, message)
            # Wait a minute to avoid resending within the same minute
            time.sleep(60)


if __name__ == "__main__":

    # Usage
    recipient_number = "+1234567890"  # Replace with the recipient's phone number
    sms_message = "This is your daily reminder to check your tasks!"

    # Uncomment this line to run the reminder on schedule
    # schedule_daily_text(recipient_number, sms_message)

    # Or send a single text message immediately
    send_text_message(recipient_number, sms_message)
