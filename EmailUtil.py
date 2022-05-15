import json
from smtplib import SMTP_SSL
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.header import Header

class EmailUtil:
    # files store sender and receiver information
    sender_settings_file = ""
    receiver_settings_file = ""

    # sender information
    from_address = ''       # sender email address
    from_address_pwd = ""   # qq mail passcode

    # receiver information
    to_address = "" # receiver email address

    def __init__(self, sender_settings_file, receiver_settings_file):
        """read custom settings from sender"""
        with open(sender_settings_file) as json_file:
            sender_info = json.load(json_file)

            self.from_address = sender_info['mailSender']
            self.from_address_pwd = sender_info['mailSenderPassword']

        """read custom setting from receiver"""
        with open(receiver_settings_file) as json_file:
            receiver_info = json.load(json_file) 

            self.to_address = receiver_info['mailReceiver']

    """email me the given message"""
    def email_me(self, subject, send_content):
        """email use qq mail"""
        host_server = 'smtp.qq.com'
        # ssl login
        smtp = SMTP_SSL(host_server)
        # set_debuglevel() for debug, 1 enable debug, 0 for disable
        # smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(self.from_address, self.from_address_pwd)

        # construct message
        msg = EmailMessage()
        msg = MIMEText(send_content, "plain", 'utf-8')
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = Header(subject, 'utf-8')
        
        to_addrs = [self.to_address]
        smtp.sendmail(self.from_address, to_addrs, msg.as_string())
        smtp.quit()