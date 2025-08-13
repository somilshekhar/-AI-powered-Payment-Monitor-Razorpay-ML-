import smtplib
from email.mime.text import MIMEText
from .config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ALERT_FROM, ALERT_TO
def send_email_alert(subject: str, body: str, to: str = None):
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ALERT_FROM]): return
    to = to or ALERT_TO or ALERT_FROM
    msg = MIMEText(body); msg["Subject"]=subject; msg["From"]=ALERT_FROM; msg["To"]=to
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(); server.login(SMTP_USER, SMTP_PASS); server.sendmail(ALERT_FROM, [to], msg.as_string())
