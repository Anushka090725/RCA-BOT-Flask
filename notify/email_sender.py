# import smtplib
# from email.mime.text import MIMEText

# def send_email(subject, body, to_email):
#     from_email = "anushkaarorabusinessnext090725@gmail.com"
#     password = "yqwj qzlv gqsq uwrj"  # Use App Password for Gmail

#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = from_email
#     msg['To'] = to_email

#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(from_email, password)
#         server.send_message(msg)
import smtplib
# print("email_sender.py")
from email.mime.text import MIMEText
from utils.config import EMAIL_SENDER, SMTP_SERVER, SMTP_PORT, SMTP_PASSWORD, DEV_EMAILS

def send_email(subject, body,to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, SMTP_PASSWORD)
        server.sendmail(EMAIL_SENDER, DEV_EMAILS, msg.as_string())