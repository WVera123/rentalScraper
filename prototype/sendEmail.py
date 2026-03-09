import smtplib
from email.mime.text import MIMEText
import datetime

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body, "html")  # HTML email

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())

    print("Message sent at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))