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

    Attributes: the target URL, time interval to detect changes, and headers (only related to monitor action)
    """

    # default monitor settings
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36'}  # act like a browser
    url = "https://leviyanx.github.io/"  # default target URL
    time_interval = 15  # default time interval to detect changes

    def __init__(self, monitor_settings_file):
        # read custom settings from monitor settings file
        with open(monitor_settings_file) as json_file:
            monitor_info = json.load(json_file)

            self.url = monitor_info['targetUrl']
            self.time_interval = monitor_info['intervalToDetect']

    def monitor_one_webpage_and_notify(self, sender_settings_file, receiver_settings_file):
        """Monitor changes in specified webpage and notify the receiver with changed content by email

        :param sender_settings_file: file stores sender's settings
        :param receiver_settings_file: file stores receiver's information
        """
        email_util = EmailUtil(sender_settings_file)
        receiver_address = EmailUtil.get_receiver_email(receiver_settings_file)
        prev_version = ""
        first_run = True
        while True:
            try:
                # download the page
                response = requests.get(self.url, headers=self.headers)
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
                        print("Start Monitoring " + self.url + "" + str(datetime.now()))
                    else:
                        print("Changes detected at: " + str(datetime.now()))
                        OldPage = prev_version.splitlines()
                        NewPage = soup.splitlines()
                        # compare versions and highlight changes using difflib
                        # d = difflib.Differ()
                        # diff = d.compare(OldPage, NewPage)
                        diff = difflib.context_diff(OldPage, NewPage, n=10)
                        out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])

                        # print and email me the changes
                        print(out_text)
                        subject = "Something new in your follow website" + self.url
                        email_util.email_specified_user(subject, out_text, receiver_address)

                        OldPage = NewPage
                        # print ('\n'.join(diff))
                        prev_version = soup

                # this is used for testing
                else:
                    print("No Changes " + str(datetime.now()))

                # time interval to run compare
                time.sleep(self.time_interval)
                continue

            except Exception as e:
                # email receiver the error message
                subject = "SOMETHING WRONG IN YOUR MONITOR!"
                send_content = self.url + '\n' + e
                email_util.email_specified_user(subject, send_content, receiver_address)

                # quit the program
                break


# load file in local machine
monitor_settings_file = 'monitor-settings.json'
sender_settings_file = 'sender-settings.json'
receiver_settings_file = 'receiver-settings.json'

# monitor
monitor = WebsiteMonitor(monitor_settings_file)
monitor.monitor_one_webpage_and_notify(sender_settings_file, receiver_settings_file)
