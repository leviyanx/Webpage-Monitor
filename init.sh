#!/usr/bin/env bash

# This script is used to generate the initial configuration files

echo "{ \"receivers\": [ \"receiver1@exmaple.com\", \"receiver2@exmaple.com\", \"...\" ] }" > receiver-settings.json

echo "{ \"mailSender\": \"<sender@qq.com/foxmail.com>\", \"mailSenderPassword\": \"<password>\" }" > sender-settings.json

echo "{ \"webpages\" : [ { \"targetUrl\" : \"<url1>\", \"intervalToDetect\" : 1800 }, { \"targetUrl\" : \"<url2>\", \"intervalToDetect\" : 1800 } ] }" > monitor-settings.json