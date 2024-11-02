import requests
import smtplib
import json
import os
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load configuration from file
with open("config.json") as config_file:
    config = json.load(config_file)

endpoint_url = config["endpoint_url"]
check_interval = config["check_interval"]
email_enabled = config["email_enabled"]
slack_enabled = config["slack_enabled"]

def send_email_notification(subject, body):
    email_config = config["email"]
    msg = MIMEMultipart()
    msg["From"] = email_config["sender_email"]
    msg["To"] = email_config["receiver_email"]
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"]) as server:
            server.starttls()
            server.login(email_config["sender_email"], email_config["sender_password"])
            server.sendmail(email_config["sender_email"], email_config["receiver_email"], msg.as_string())
        print("Email notification sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_slack_notification(message):
    slack_webhook_url = config["slack"]["webhook_url"]
    slack_message = {"text": message}

    try:
        response = requests.post(slack_webhook_url, json=slack_message)
        response.raise_for_status()
        print("Slack notification sent.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Slack notification: {e}")

def check_health():
    try:
        response = requests.get(endpoint_url, timeout=10)
        if response.status_code == 200:
            print(f"Endpoint {endpoint_url} is up.")
        else:
            print(f"Endpoint {endpoint_url} is down. Status code: {response.status_code}")
            notify("Endpoint is down!")
    except requests.exceptions.RequestException as e:
        print(f"Health check failed: {e}")
        notify("Health check failed: Unable to reach the endpoint.")

def notify(message):
    if email_enabled:
        send_email_notification("Endpoint Down Alert", message)
    if slack_enabled:
        send_slack_notification(message)

if __name__ == "__main__":
    while True:
        check_health()
        sleep(check_interval)

