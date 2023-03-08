#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime
import json
from EmailUtil import EmailUtil


class WebsiteMonitor:
    """ This class is used to monitor changes in a website"""

    # default monitor settings
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36'}  # act like a browser
    url = "https://leviyanx.github.io/"  # default target URL
    time_interval = 15  # default time interval to detect changes

    # email settings
    sender_settings_file = ""
    receiver_settings_file = ""

    def __init__(self, monitor_settings_file, sender_settings_file, receiver_settings_file):
        # read custom settings from monitor settings file
        with open(monitor_settings_file) as json_file:
            monitor_info = json.load(json_file)

            self.url = monitor_info['targetUrl']
            self.time_interval = monitor_info['intervalToDetect']

        self.sender_settings_file = sender_settings_file
        self.receiver_settings_file = receiver_settings_file

    def monitor_one_website(self):
        """monitor changes in website and show us what changed and email me the change"""
        emailUtil = EmailUtil(self.sender_settings_file, self.receiver_settings_file)
        PrevVersion = ""
        FirstRun = True
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
                if PrevVersion != soup:
                    # on the first run - just memorize the page
                    if FirstRun == True:
                        PrevVersion = soup
                        FirstRun = False
                        print("Start Monitoring " + self.url + "" + str(datetime.now()))
                    else:
                        print("Changes detected at: " + str(datetime.now()))
                        OldPage = PrevVersion.splitlines()
                        NewPage = soup.splitlines()
                        # compare versions and highlight changes using difflib
                        # d = difflib.Differ()
                        # diff = d.compare(OldPage, NewPage)
                        diff = difflib.context_diff(OldPage, NewPage, n=10)
                        out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])

                        # print and email me the changes
                        print(out_text)
                        subject = "Something new in your follow website" + self.url
                        emailUtil.email_me(subject, out_text)

                        OldPage = NewPage
                        # print ('\n'.join(diff))
                        PrevVersion = soup

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
                emailUtil.email_me(subject, send_content)

                # quit the program
                break


# load file in local machine
monitor_settings_file = 'monitor-settings.json'
sender_settings_file = 'sender-settings.json'
receiver_settings_file = 'receiver-settings.json'

# monitor
monitor = WebsiteMonitor(monitor_settings_file, sender_settings_file, receiver_settings_file)
monitor.monitor_one_website()
