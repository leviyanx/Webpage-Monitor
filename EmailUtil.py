import json
from smtplib import SMTP_SSL
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.header import Header


class EmailUtil:
    """email util class

    Attributes: only one attribute, the sender email address and password
    """

    def __init__(self, sender_settings_file: str):
        from_address, from_address_passwd = self.get_sender_settings(sender_settings_file)
        self.from_address = from_address
        self.from_address_pwd = from_address_passwd

    @staticmethod
    def get_sender_settings(sender_settings_file: str):
        """get sender email address and password from json file"""
        with open(sender_settings_file) as json_file:
            sender_info = json.load(json_file)

            return sender_info['mailSender'], sender_info['mailSenderPassword']

    @staticmethod
    def get_receiver_email(receiver_settings_file: str):
        """get receiver email address from json file"""
        with open(receiver_settings_file) as json_file:
            receiver_info = json.load(json_file)

            return receiver_info['mailReceiver']

    def email_specified_receiver(self, subject: str, send_content: str, to_address):
        """email specified user the given message"""

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
        msg['To'] = to_address
        msg['Subject'] = Header(subject, 'utf-8')

        smtp.sendmail(self.from_address, to_address, msg.as_string())

        smtp.quit()
