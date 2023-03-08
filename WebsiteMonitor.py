#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime
import json
from EmailUtil import EmailUtil


class WebsiteMonitor:
    """ This class is used to monitor changes in a website

    Attributes: only one attribute, the headers to act like a browser
    """

    def __init__(self):
        # default monitor settings
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36'}  # act like a browser

    @staticmethod
    def get_monitor_settings(monitor_settings_file):
        """get monitor settings from json file"""
        with open(monitor_settings_file) as json_file:
            monitor_info = json.load(json_file)

            return monitor_info['targetUrl'], monitor_info['intervalToDetect']

    def monitor_one_webpage_and_notify(self, monitor_settings_file, sender_settings_file, receiver_settings_file):
        """Monitor changes in specified webpage and notify the receiver with changed content by email. \n
        Only load the email when needed, so that user don't need to restart the script when only email settings (sender
        and receiver) are changed.

        :param monitor_settings_file: file stores monitor settings (target URL and time interval)
        :param sender_settings_file: file stores sender's settings (email address and password)
        :param receiver_settings_file: file stores receiver's information (email address)
        """
        prev_version = ""
        first_run = True
        while True:
            try:
                # Except the first time, every other time, after time interval the script will load the monitor settings again
                target_url, time_interval = self.get_monitor_settings(monitor_settings_file)

                # download the page
                response = requests.get(target_url, headers=self.headers)
                # parse the downloaded homepage
                soup = BeautifulSoup(response.text, "lxml")

                # remove all scripts and styles
                for script in soup(["script", "style"]):
                    script.extract()
                soup = soup.get_text()
                # compare the page text to the previous version
                if prev_version != soup:
                    # on the first run - just memorize the page
                    if first_run == True:
                        prev_version = soup
                        first_run = False
                        print("Start Monitoring " + target_url + "" + str(datetime.now()))
                    else:
                        print("Changes detected at: " + str(datetime.now()))
                        OldPage = prev_version.splitlines()
                        NewPage = soup.splitlines()
                        diff = difflib.context_diff(OldPage, NewPage, n=10)
                        out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])

                        # print and email me the changes
                        print(out_text)
                        email_util = EmailUtil(sender_settings_file)
                        receiver_address = EmailUtil.get_receiver_email(receiver_settings_file)
                        subject = "Something new in your follow website" + target_url
                        email_util.email_specified_receiver(subject, out_text, receiver_address)

                        OldPage = NewPage
                        # print ('\n'.join(diff))
                        prev_version = soup

                # this is used for testing
                else:
                    print("No Changes " + str(datetime.now()))

                # time interval to run compare
                time.sleep(time_interval)
                continue

            except Exception as e:
                # notify receiver with the error message
                email_util = EmailUtil(sender_settings_file)
                receiver_address = EmailUtil.get_receiver_email(receiver_settings_file)
                subject = "SOMETHING WRONG IN YOUR MONITOR!"
                target_url, _ = self.get_monitor_settings(monitor_settings_file)
                error_message = target_url + '\n' + e

                email_util.email_specified_receiver(subject, error_message, receiver_address)

                # quit the program
                break


# load file in local machine
monitor_settings_file = 'monitor-settings.json'
sender_settings_file = 'sender-settings.json'
receiver_settings_file = 'receiver-settings.json'

# monitor
monitor = WebsiteMonitor()
monitor.monitor_one_webpage_and_notify(monitor_settings_file, sender_settings_file, receiver_settings_file)
