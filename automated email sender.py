import smtplib
from email.mime.text import MIMEText

# Your Gmail credentials (use App Password)
GMAIL_USER = 'test@gmail.com'
GMAIL_PASS = 'app password'

# Email content
SUBJECT = "I help businesses work smarter – free consult"
BODY = """Hi, test email

"""

# Load recipients
with open("emails.txt", "r", encoding="utf-8") as f:
    recipients = [line.strip() for line in f if line.strip()]

# Send email to each recipient
def send_email(to_email):
    msg = MIMEText(BODY)
    msg['Subject'] = SUBJECT
    msg['From'] = GMAIL_USER
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
            print(f"✅ Sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")

# Run loop
for email in recipients:
    send_email(email)
