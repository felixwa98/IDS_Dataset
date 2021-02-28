from email.mime import text
import random
from configparser import SafeConfigParser
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)
import Packages.logging.log_file as log

def choose_random_line(xlist):
    lines = open(xlist).read().splitlines()
    return random.choice(lines)

def get_server_info(smtpserver):
    parser = SafeConfigParser()
    parser.read(smtpserver)

    ip = parser["EMAIL"]["ip"]
    port = parser["EMAIL"]["port"]
    sender_email = parser["EMAIL"]["sender"]
    password = parser["EMAIL"]["password"]

    return ip, sender_email, password, port

def main(smtpserver, destinationaddresslist, bodylist, subjectlist, attachmentslist):

    serverinfo = get_server_info(smtpserver)

    subject = choose_random_line(subjectlist)
    body = choose_random_line(bodylist)
    sender_email = serverinfo[1]
    receiver_email = choose_random_line(destinationaddresslist)
    password = serverinfo[2]

    serverip = serverinfo[0]
    serverport = serverinfo[3]
    filename = choose_random_line(attachmentslist)  # In same directory as script

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Decide wheater an attachment should be sent
    if(random.randint(1,10) < 7):
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(serverip, int(serverport), context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    log.log_event("Emali send;" + receiver_email)
    