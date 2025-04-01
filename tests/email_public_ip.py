"""Send email with public ip address
For Dencam, there is an interest in obtaining internet
connectivity via Starlink. Because we would be power cycling
the Starlink daily to conserve power, the Pi should send
an email whenever the Starlink wakes up with the public IP for that
session. It's unclear if our current Starlink plan supports remote
SSH or even has a public IP, but this can be used to troubleshoot.

Usage:
For sending after network is aquired after a reboot:

sudo nano /etc/systemd/system/send_ip.service

'''[Unit]
Description=My script that requires network
After=network.target

[Service]
Type=oneshot
ExecStart= /usr/bin/python3 /home/USER/dencam_hardware/tests/email_public_ip.py

[Install]
WantedBy=multi-user.target'''

sudo systemctl daemon-reload
sudo systemctl enable send_ip

"""

import smtplib
from email.mime.text import MIMEText
import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='starlink_ip.log', encoding='utf-8', level=logging.DEBUG)

SMTP_SERVER = 'smtp.gmail.com' # if using gmail
SMTP_PORT = 587
EMAIL_ADDRESS = '<INSERT EMAIL>'
EMAIL_PASSWORD = '<INSERT APP PASSWORD>'
TO_EMAIL = '<INSERT RECEIVER EMAIL>'

def get_public_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        logger.info(f"IP address: {ip}")
        return ip
    except Exception as e:
        logger.warning(f"Failed to get IP: {e}")
        return f"Failed to get IP: {e}"

def send_email(ip_address):
    subject = "Starlink Public IP"
    body = f"Your current public IP is: {ip_address}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info("Email sent successfully.")
    except Exception as e:
        logger.warning(f"Failed to send email: {e}")

if __name__ == '__main__':
    ip = get_public_ip()
    send_email(ip)
