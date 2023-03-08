#!/usr/bin/env bash

# This script is used to generate the initial configuration files

echo "{ \"mailReceiver\": \"<receiver@mail.com>\" }" > receiver-settings.json

echo "{ \"mailSender\": \"<sender@qq.com/foxmail.com>\", \"mailSenderPassword\": \"<password>\" }" > sender-settings.json

echo "{ \"targetUrl\": \"<http://example.com/url-of-target-webpage>\", \"intervalToDetect\": 1800 }" > monitor-settings.json