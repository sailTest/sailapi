import smtplib
import ssl 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmail(sender_email, receiver_email, subject, message_body, smtp_server, smtp_port, smtp_username, smtp_password):
    # Create a MIME object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the message body
    message.attach(MIMEText(message_body, 'html','utf-8'))

    context = ssl.create_default_context()


    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        # Log in to the SMTP server if authentication is required
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

def emailCompose(subject,filename):
    sender_email = "al_785@hotmail.com"
    receiver_email = "alden.97@gmail.com"
    #message_body = "This is the body of the email, and a test."
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    smtp_username = "al_785@hotmail.com"
    smtp_password = "(#t3chn01sl0v3)"
    with open(filename,"r") as attachinfo:
        message_bdy = attachinfo.read()


    sendEmail(sender_email, receiver_email, subject,message_bdy, smtp_server, smtp_port, smtp_username, smtp_password)
    

if __name__ == "__main__":
    # Replace these values with your email and SMTP server information
    sender_email = "al_785@hotmail.com"
    receiver_email = "alden.97@gmail.com"
    #subject = "L"
    #message_body = "This is the body of the email, and a test."
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    smtp_username = "al_785@hotmail.com"
    smtp_password = ""

    sendEmail(sender_email, receiver_email, emailCompose[1],emailCompose(2), smtp_server, smtp_port, smtp_username, smtp_password)
