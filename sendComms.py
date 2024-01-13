import smtplib
import ssl 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, subject, message_body, smtp_server, smtp_port, smtp_username, smtp_password):
    # Create a MIME object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the message body
    message.attach(MIMEText(message_body, 'plain'))

    context = ssl.create_default_context()


    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        # Log in to the SMTP server if authentication is required
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == "__main__":
    # Replace these values with your email and SMTP server information
    sender_email = "al_785@hotmail.com"
    receiver_email = "alden.97@gmail.com"
    subject = "Sail Test Email"
    message_body = "This is the body of the email, and a test."
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    smtp_username = "al_785@hotmail.com"
    smtp_password = ""

    send_email(sender_email, receiver_email, subject, message_body, smtp_server, smtp_port, smtp_username, smtp_password)
