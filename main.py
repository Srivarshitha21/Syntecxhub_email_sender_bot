import smtplib
import csv
import time
import logging
import os

from dotenv import load_dotenv
from email.message import EmailMessage

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASS")

# Check if credentials exist
if not EMAIL_ADDRESS or not APP_PASSWORD:
    print("Error: EMAIL_USER or EMAIL_PASS not found in .env file")
    exit()

# Logging setup
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Function to send email
def send_email(name, receiver_email):

    msg = EmailMessage()

    msg["Subject"] = "Python Internship Project"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    body = f"""
Hello {name},

This is an automated email sent using Python.

Regards,
Srivarshitha
"""

    msg.set_content(body)

    # Add attachment
    filename = "attachment.pdf"

    try:
        with open(filename, "rb") as file:
            file_data = file.read()
            file_name = file.name

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_name
        )

    except FileNotFoundError:
        print(f"Warning: {filename} not found")
        logging.warning(f"{filename} not found")

    # Retry logic
    retries = 3

    for attempt in range(retries):

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

                smtp.login(EMAIL_ADDRESS, APP_PASSWORD)
                smtp.send_message(msg)

            print(f"Email sent to {receiver_email}")
            logging.info(f"SUCCESS: {receiver_email}")

            return

        except Exception as e:

            print(f"Attempt {attempt+1} failed: {e}")
            logging.error(
                f"FAILED: {receiver_email} - {e}"
            )

            time.sleep(3)

    print(f"Could not send email to {receiver_email}")


# Read recipients from CSV
try:

    with open("recipients.csv", newline='', encoding="utf-8") as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            name = row["name"]
            email = row["email"]

            send_email(name, email)

    print("All emails processed")

except FileNotFoundError:
    print("Error: recipients.csv file not found")