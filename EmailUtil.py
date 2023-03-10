import json
from smtplib import SMTP_SSL
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.header import Header


def notify(sender_settings_file: str, receiver_settings_file: str, subject: str, content: str):
    """notify receiver with the given message (using sender's email address)

    :param sender_settings_file: file stores sender's settings (email address and password)
    :param receiver_settings_file: file stores receiver's information (email address)
    :param subject: subject of the email
    :param content: content of the email
    """
    email_util = EmailUtil(sender_settings_file)
    email_util.email_specified_receiver(receiver_settings_file, subject, content)


class EmailUtil:
    """email util class, take responsibility of sending email

    """
    from_address = None
    from_address_pwd = None
    receivers = None

    def __init__(self, sender_settings_file: str):
        # initialize sender
        self.set_sender_settings(sender_settings_file)

    def set_sender_settings(self, sender_settings_file: str):
        """set sender settings from json file"""
        with open(sender_settings_file) as json_file:
            sender_info = json.load(json_file)

            self.from_address = sender_info['mailSender']
            self.from_address_pwd = sender_info['mailSenderPassword']

    def get_receiver_email_address(self, receiver_settings_file: str):
        """get receiver email address from json file"""
        with open(receiver_settings_file) as json_file:
            receiver_info = json.load(json_file)

            self.receivers = receiver_info['receivers']

    def email_specified_receiver(self, address_file: str, subject: str, send_content: str):
        """Email specified users the given message"""

        # ssl login
        host_server = 'smtp.qq.com'  # email use qq mail
        smtp = SMTP_SSL(host_server)
        # set_debuglevel() for debug, 1 enable debug, 0 for disable
        # smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(self.from_address, self.from_address_pwd)

        # construct message
        msg = EmailMessage()
        msg = MIMEText(send_content, "plain", 'utf-8')
        msg['From'] = self.from_address
        self.get_receiver_email_address(address_file)
        to_address = ','.join(self.receivers)
        msg['To'] = to_address
        msg['Subject'] = Header(subject, 'utf-8')

        smtp.sendmail(self.from_address, to_address, msg.as_string())

        smtp.quit()
