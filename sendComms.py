####################################################################################
#                                                                                  #
# Author: Aldo Mestas                                                              #
# Script which handles the communication with an email server and sends  .         #
# the output from query the github API for a set of specific PR's                  #
#                                                                                  #
# January 2024                                                                     #
#                                                                                  # 
#                                                                                  #
####################################################################################

import smtplib
import ssl 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from setUpVariables import sender_email, receiver_email, smtp_server, smtp_port, smtp_username, smtp_password

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
    senderEmail = sender_email
    receiverEmail = receiver_email
    smtpServer = smtp_server
    smtpPort = smtp_port
    smtpUsername = smtp_username
    smtpPassword = smtp_password
    # It deemed easier send it as a file
    with open(filename,"r") as attachinfo:
        message_bdy = attachinfo.read()
    attachinfo.close()

    sendEmail(senderEmail, receiverEmail, subject,message_bdy, smtpServer, smtpPort, smtpUsername, smtpPassword)
    
