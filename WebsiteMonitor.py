#!/usr/bin/env python3
import threading
import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime
import json
from EmailUtil import EmailUtil


class WebsiteMonitor:
    """ This class is used to monitor changes in a website and notify the changes by email.

    Attributes: only one attribute, the headers to act like a browser
    """

    def __init__(self):
        # default monitor settings
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36'}  # act like a browser
        self.exit_flag = False  # flag to exit the monitor thread

    def monitor_multiple_webpages_and_notify(self, monitor_settings_file, sender_settings_file, receiver_settings_file):
        """
        Monitor changes in multiple webpages and notify the receiver with changed content by email. \n
        Automatically reload monitor settings in every one and half hour. \n

        :param monitor_settings_file: file stores monitor settings of webpages
        :param sender_settings_file: file stores sender's settings (email address and password)
        :param receiver_settings_file: file stores receiver's information (email address)
        """
        threads = []
        self.exit_flag = False
        while True:
            try:
                # get the monitor settings of webpages
                webpages = self.get_monitor_settings_of_webpages(monitor_settings_file)['webpages']

                # start monitor every webpage
                for webpage in webpages:
                    # one thread for one webpage
                    thread = threading.Thread(target=self.monitor_one_webpage_and_notify, args=(
                    webpage['targetUrl'], webpage['intervalToDetect'], sender_settings_file, receiver_settings_file))
                    threads.append(thread)
                # start all threads
                for thread in threads:
                    thread.start()

                # wait for one hour
                time.sleep(3600)
                # It's time to exit all monitor threads
                self.exit_flag = True
                for thread in threads:
                    thread.join()

                # reset the exit flag and start a new round of monitor
                self.exit_flag = False

            except Exception as e:
                # notify receiver with the error message
                subject = "SOMETHING WRONG IN YOUR MONITOR!"
                error_message = "Error in monitor multiple webpages: " + e
                self.notify(sender_settings_file, receiver_settings_file, subject, error_message)

                # quit the program
                break

    def monitor_one_webpage_and_notify(self, target_url, time_interval, sender_settings_file, receiver_settings_file):
        """Monitor changes in one specified webpage and notify the receiver with changed content by email. \n
        Only load the email when needed, so that user don't need to restart the script when only email settings (sender
        and receiver) are changed.

        :param target_url: url of the target webpage
        :param time_interval: time interval to monitor
        :param sender_settings_file: file stores sender's settings (email address and password)
        :param receiver_settings_file: file stores receiver's information (email address)
        """
        prev_page_content = ""
        first_run = True
        while not self.exit_flag:
            try:
                current_page_content = self.get_target_page_text(target_url)

                # compare the current page text to the previous
                if prev_page_content != current_page_content:
                    if first_run:
                        # on the first run - just memorize the page
                        prev_page_content = current_page_content
                        first_run = False
                        print("Start Monitoring " + target_url + "" + str(datetime.now()) + "\n")
                    else:
                        print("Changes detected at: " + str(datetime.now()) + "\n")
                        OldPage = prev_page_content.splitlines()
                        NewPage = current_page_content.splitlines()
                        diff = difflib.context_diff(OldPage, NewPage, n=10)
                        out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])

                        # print the changes
                        print(out_text)
                        # notify receiver with the changes
                        subject = "Something new in your follow website" + target_url
                        self.notify(sender_settings_file, receiver_settings_file, subject, out_text)

                        OldPage = NewPage
                        # print ('\n'.join(diff))
                        prev_page_content = current_page_content

                # this is used for testing
                else:
                    print("No Changes " + str(datetime.now()) + "\n")

                # time interval to run compare
                time.sleep(time_interval)
                continue

            except Exception as e:
                # notify receiver with the error message
                subject = "SOMETHING WRONG IN YOUR MONITOR!"
                error_message = target_url + '\n' + e
                self.notify(sender_settings_file, receiver_settings_file, subject, error_message)

                # quit the program
                break

    @staticmethod
    def get_monitor_settings_of_webpages(monitor_settings_file):
        """get monitor settings of webpages from json file"""
        with open(monitor_settings_file) as json_file:
            monitor_settings = json.load(json_file)
            return monitor_settings

    def get_target_page_text(self, target_url):
        """get the text of the target webpage"""
        # download the page
        response = requests.get(target_url, headers=self.headers)

        # parse the downloaded homepage
        soup = BeautifulSoup(response.text, "lxml")

        # remove all scripts and styles
        for script in soup(["script", "style"]):
            script.extract()

        return soup.get_text()

    @staticmethod
    def notify(sender_settings_file, receiver_settings_file, subject, content):
        """notify receiver with the given message (using sender's email address)

        :param sender_settings_file: file stores sender's settings (email address and password)
        :param receiver_settings_file: file stores receiver's information (email address)
        :param subject: subject of the email
        :param content: content of the email
        """
        email_util = EmailUtil(sender_settings_file)
        receiver_address = EmailUtil.get_receiver_email(receiver_settings_file)
        email_util.email_specified_receiver(subject, content, receiver_address)
