#!/usr/bin/env python3
import threading
import requests
from bs4 import BeautifulSoup
import difflib
import time
import json
import EmailUtil
import logging

logging.basicConfig(filename="execution.log", encoding="utf-8",
                    level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


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

    def monitor_multiple_webpages_and_notify(self, monitor_settings_file: str, sender_settings_file: str,
                                             receiver_settings_file: str):
        """
        Monitor changes in multiple webpages and notify the receiver with changed content by email. \n
        Automatically reload monitor settings in every 90 minutes. \n

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
                        webpage['targetUrl'], webpage['intervalToDetect'], sender_settings_file,
                        receiver_settings_file))
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

                # start a new round of monitor
                self.exit_flag = False  # reset the exit flag and
                threads = []  # reset the threads list

            except Exception as e:
                error_message = "Error in monitor multiple webpages"
                logging.error(error_message)
                logging.exception(e)
                # notify receiver with the error message
                subject = "SOMETHING WRONG IN YOUR MONITOR!"
                EmailUtil.notify(sender_settings_file, receiver_settings_file, subject, error_message)

                # quit the program
                break

    def monitor_one_webpage_and_notify(self, target_url: str, time_interval: int, sender_settings_file: str,
                                       receiver_settings_file: str):
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
                        logging.info("Start Monitoring " + target_url)
                    else:
                        logging.info("Changes detected at " + target_url)
                        OldPage = prev_page_content.splitlines()
                        NewPage = current_page_content.splitlines()
                        diff = difflib.context_diff(OldPage, NewPage, n=10)
                        out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])

                        logging.info("Notifying")
                        # notify receiver with the changes
                        subject = "Something new in your follow website" + target_url
                        EmailUtil.notify(sender_settings_file, receiver_settings_file, subject, out_text)

                        prev_page_content = current_page_content

                # time interval to run compare
                time.sleep(time_interval)
                continue

            except Exception as e:
                error_message = "Error in monitoring the webpage: " + target_url
                logging.error(error_message)
                logging.exception(e)
                # notify receiver with the error message
                subject = "SOMETHING WRONG IN YOUR MONITOR!"
                EmailUtil.notify(sender_settings_file, receiver_settings_file, subject, error_message)

                # quit the program
                break

    @staticmethod
    def get_monitor_settings_of_webpages(monitor_settings_file: str):
        """get monitor settings of webpages from json file"""
        with open(monitor_settings_file) as json_file:
            monitor_settings = json.load(json_file)
            return monitor_settings

    def get_target_page_text(self, target_url: str):
        """get the text of the target webpage"""
        # download the page
        response = requests.get(target_url, headers=self.headers)

        # parse the downloaded homepage
        soup = BeautifulSoup(response.text, "lxml")

        # remove all scripts and styles
        for script in soup(["script", "style"]):
            script.extract()

        return soup.get_text()
