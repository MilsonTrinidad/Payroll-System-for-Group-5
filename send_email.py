import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_message(sender_email, sender_password, receiver_email, subject, body, file_path, file_name):
    # Set up MIME to initialize the email's format
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Provide File for email
    attachment = open(file_path, "rb")
    base = MIMEBase("application", "octet-stream")
    base.set_payload(attachment.read())
    encoders.encode_base64(base)
    base.add_header("Content-Disposition", f"attachment; filename={file_name}")
    message.attach(base)

    # Connects to the SMTP server
    smtp_server = "smtp.gmail.com" 
    smtp_port = 587
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        # print("Email sent successfully.")

    except Exception as e:
        print(f"Error: {e}")